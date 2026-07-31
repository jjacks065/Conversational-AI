"""Strict, platform-neutral YAML configuration loading."""

from __future__ import annotations

import ipaddress
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when proxy configuration is missing, unsafe, or invalid."""


@dataclass(frozen=True)
class ProxyConfig:
    listen_host: str
    listen_port: int
    fail_open: bool
    max_buffer_bytes: int


@dataclass(frozen=True)
class TargetConfig:
    scheme: str
    host: str
    port: int
    methods: tuple[str, ...]
    paths: tuple[str, ...]
    request_content_types: tuple[str, ...]
    response_content_types: tuple[str, ...]


@dataclass(frozen=True)
class MatchingConfig:
    required_request_headers: Mapping[str, str]


@dataclass(frozen=True)
class TransformationConfig:
    enabled: bool
    mode: str
    preserve_unknown_fields: bool
    transformer_version: str


@dataclass(frozen=True)
class LoggingConfig:
    level: str
    log_request_bodies: bool
    log_response_bodies: bool
    log_match_decisions: bool
    redact_headers: frozenset[str]


@dataclass(frozen=True)
class PlatformConfig:
    browser_profile_name: str
    health_port: int
    pac_port: int


@dataclass(frozen=True)
class AppConfig:
    proxy: ProxyConfig
    target: TargetConfig
    matching: MatchingConfig
    transformation: TransformationConfig
    logging: LoggingConfig
    platform: PlatformConfig


_ROOT_KEYS = {
    "proxy",
    "target",
    "matching",
    "transformation",
    "logging",
    "platform",
}
_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def normalize_media_type(value: str) -> str:
    """Return a lower-case media type without parameters."""

    normalized = value.split(";", 1)[0].strip().lower()
    if normalized.count("/") != 1 or any(char.isspace() for char in normalized):
        raise ConfigError(f"invalid media type: {value!r}")
    return normalized


def load_config(path: str | Path) -> AppConfig:
    """Load and validate a UTF-8 YAML configuration file."""

    config_path = Path(path)
    try:
        source = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"unable to read configuration: {config_path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"invalid YAML configuration: {config_path}") from exc
    return parse_config(source)


def parse_config(source: object) -> AppConfig:
    """Validate a parsed configuration mapping without modifying it."""

    root = _as_mapping(source, "configuration")
    _reject_unknown_keys(root, _ROOT_KEYS, "configuration")
    for section_name in _ROOT_KEYS:
        if section_name not in root:
            raise ConfigError(f"missing section: {section_name}")

    proxy_source = _section(
        root,
        "proxy",
        {"listen_host", "listen_port", "fail_open", "max_buffer_bytes"},
    )
    target_source = _section(
        root,
        "target",
        {
            "scheme",
            "host",
            "port",
            "methods",
            "paths",
            "request_content_types",
            "response_content_types",
        },
    )
    matching_source = _section(root, "matching", {"required_request_headers"})
    transformation_source = _section(
        root,
        "transformation",
        {"enabled", "mode", "preserve_unknown_fields", "transformer_version"},
    )
    logging_source = _section(
        root,
        "logging",
        {
            "level",
            "log_request_bodies",
            "log_response_bodies",
            "log_match_decisions",
            "redact_headers",
        },
    )
    platform_source = _section(
        root,
        "platform",
        {"browser_profile_name", "health_port", "pac_port"},
    )

    listen_host = _required_string(proxy_source, "listen_host", "proxy")
    if not _is_loopback(listen_host):
        raise ConfigError("proxy.listen_host must resolve to a loopback literal or localhost")
    listen_port = _required_port(proxy_source, "listen_port", "proxy")
    max_buffer_bytes = _required_int(
        proxy_source, "max_buffer_bytes", "proxy", minimum=1
    )
    proxy = ProxyConfig(
        listen_host=listen_host,
        listen_port=listen_port,
        fail_open=_required_bool(proxy_source, "fail_open", "proxy"),
        max_buffer_bytes=max_buffer_bytes,
    )

    scheme = _required_string(target_source, "scheme", "target").lower()
    if scheme not in {"http", "https"}:
        raise ConfigError("target.scheme must be http or https")
    host = _required_string(target_source, "host", "target").lower()
    if "://" in host or "/" in host:
        raise ConfigError("target.host must contain only a hostname")
    methods = tuple(
        value.upper() for value in _required_string_list(target_source, "methods", "target")
    )
    paths = _required_string_list(target_source, "paths", "target")
    for pattern in paths:
        _validate_regex(pattern, "target.paths")
    target = TargetConfig(
        scheme=scheme,
        host=host,
        port=_required_port(target_source, "port", "target"),
        methods=methods,
        paths=paths,
        request_content_types=tuple(
            normalize_media_type(value)
            for value in _required_string_list(
                target_source, "request_content_types", "target"
            )
        ),
        response_content_types=tuple(
            normalize_media_type(value)
            for value in _required_string_list(
                target_source, "response_content_types", "target"
            )
        ),
    )

    headers_source = _as_mapping(
        _required(matching_source, "required_request_headers", "matching"),
        "matching.required_request_headers",
    )
    if not headers_source:
        raise ConfigError("matching.required_request_headers must not be empty")
    headers: dict[str, str] = {}
    for raw_name, raw_pattern in headers_source.items():
        if not isinstance(raw_name, str) or not raw_name.strip():
            raise ConfigError("matching header names must be non-empty strings")
        if not isinstance(raw_pattern, str) or not raw_pattern:
            raise ConfigError("matching header patterns must be non-empty strings")
        _validate_regex(raw_pattern, f"matching.required_request_headers.{raw_name}")
        headers[raw_name.strip().lower()] = raw_pattern
    matching = MatchingConfig(MappingProxyType(headers))

    mode = _required_string(transformation_source, "mode", "transformation")
    if mode != "deterministic":
        raise ConfigError("transformation.mode must be deterministic")
    preserve_unknown_fields = _required_bool(
        transformation_source, "preserve_unknown_fields", "transformation"
    )
    if not preserve_unknown_fields:
        raise ConfigError("transformation.preserve_unknown_fields must be true")
    transformation = TransformationConfig(
        enabled=_required_bool(transformation_source, "enabled", "transformation"),
        mode=mode,
        preserve_unknown_fields=preserve_unknown_fields,
        transformer_version=_required_string(
            transformation_source, "transformer_version", "transformation"
        ),
    )

    level = _required_string(logging_source, "level", "logging").upper()
    if level not in _LOG_LEVELS:
        raise ConfigError(f"logging.level must be one of {sorted(_LOG_LEVELS)}")
    log_request_bodies = _required_bool(
        logging_source, "log_request_bodies", "logging"
    )
    log_response_bodies = _required_bool(
        logging_source, "log_response_bodies", "logging"
    )
    if log_request_bodies or log_response_bodies:
        raise ConfigError("logging body flags must be false")
    logging_config = LoggingConfig(
        level=level,
        log_request_bodies=log_request_bodies,
        log_response_bodies=log_response_bodies,
        log_match_decisions=_required_bool(
            logging_source, "log_match_decisions", "logging"
        ),
        redact_headers=frozenset(
            value.lower()
            for value in _required_string_list(
                logging_source, "redact_headers", "logging"
            )
        ),
    )

    health_port = _required_port(platform_source, "health_port", "platform")
    pac_port = _required_port(platform_source, "pac_port", "platform")
    if len({listen_port, health_port, pac_port}) != 3:
        raise ConfigError("proxy, health, and PAC ports must be distinct")
    platform = PlatformConfig(
        browser_profile_name=_required_string(
            platform_source, "browser_profile_name", "platform"
        ),
        health_port=health_port,
        pac_port=pac_port,
    )

    return AppConfig(
        proxy=proxy,
        target=target,
        matching=matching,
        transformation=transformation,
        logging=logging_config,
        platform=platform,
    )


def _section(
    root: Mapping[str, Any], name: str, allowed_keys: set[str]
) -> Mapping[str, Any]:
    section = _as_mapping(_required(root, name, "configuration"), name)
    _reject_unknown_keys(section, allowed_keys, name)
    return section


def _as_mapping(value: object, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigError(f"{path} must be a mapping")
    return value


def _reject_unknown_keys(
    source: Mapping[str, Any], allowed: set[str], path: str
) -> None:
    unknown = sorted(str(key) for key in source if key not in allowed)
    if unknown:
        raise ConfigError(f"unknown key in {path}: {unknown[0]}")


def _required(source: Mapping[str, Any], key: str, path: str) -> Any:
    if key not in source:
        raise ConfigError(f"missing value: {path}.{key}")
    return source[key]


def _required_string(source: Mapping[str, Any], key: str, path: str) -> str:
    value = _required(source, key, path)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{path}.{key} must be a non-empty string")
    return value.strip()


def _required_string_list(
    source: Mapping[str, Any], key: str, path: str
) -> tuple[str, ...]:
    value = _required(source, key, path)
    if not isinstance(value, list) or not value:
        raise ConfigError(f"{path}.{key} must be a non-empty list")
    strings: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ConfigError(f"{path}.{key} must contain non-empty strings")
        strings.append(item.strip())
    return tuple(dict.fromkeys(strings))


def _required_bool(source: Mapping[str, Any], key: str, path: str) -> bool:
    value = _required(source, key, path)
    if not isinstance(value, bool):
        raise ConfigError(f"{path}.{key} must be a boolean")
    return value


def _required_int(
    source: Mapping[str, Any], key: str, path: str, *, minimum: int
) -> int:
    value = _required(source, key, path)
    if type(value) is not int or value < minimum:
        raise ConfigError(f"{path}.{key} must be an integer >= {minimum}")
    return value


def _required_port(source: Mapping[str, Any], key: str, path: str) -> int:
    value = _required_int(source, key, path, minimum=1)
    if value > 65_535:
        raise ConfigError(f"{path}.{key} must be between 1 and 65535")
    return value


def _validate_regex(pattern: str, path: str) -> None:
    try:
        re.compile(pattern)
    except re.error as exc:
        raise ConfigError(f"invalid regular expression at {path}") from exc


def _is_loopback(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False
