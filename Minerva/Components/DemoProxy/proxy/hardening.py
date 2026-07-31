"""Deterministic demo preflight, drift, package, and live-listener auditing."""

from __future__ import annotations

import hashlib
import json
import socket
import tarfile
import urllib.request
import zipfile
from collections.abc import Callable, Mapping
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .config import AppConfig, ConfigError, load_config, parse_config
from .logging_config import EVENT_FIELDS


class HardeningError(RuntimeError):
    """Raised when a demo hardening invariant is not satisfied."""


_REQUIRED_REDACTIONS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "ocp-apim-subscription-key",
}
_FORBIDDEN_EVENT_FIELDS = {
    "authorization",
    "cookie",
    "headers",
    "message",
    "prompt",
    "request_body",
    "response_body",
}
_FORBIDDEN_SCRIPT_TOKENS = {
    "--proxy-server",
    "/Library/LaunchDaemons",
    "Internet Settings",
    "LocalMachine\\Root",
    "Set-ItemProperty",
    "System.keychain",
    "killall",
    "netsh",
    "networksetup",
    "pkill",
    "sudo",
    "taskkill",
}
_FORBIDDEN_ARCHIVE_FRAGMENTS = {
    ".key",
    ".pem",
    ".pfx",
    ".venv",
    "Content-Sample",
    "PROTOCOL_DISCOVERY",
    "chrome-profile",
    "runtime/",
    "tests/",
}


def audit_hardening(
    *,
    project_root: Path,
    config_path: Path,
    lock_path: Path,
    artifact_path: Path | None = None,
    live: bool = False,
) -> dict[str, Any]:
    """Audit frozen rules and optional package/live runtime state."""

    project_root = project_root.resolve()
    try:
        config = load_config(config_path)
    except ConfigError as exc:
        raise HardeningError(f"configuration failed hardening validation: {exc}") from exc
    rules = frozen_rules(config)
    lock = _load_json(lock_path, "demo rule lock")
    if lock.get("formatVersion") != 1 or not isinstance(lock.get("rules"), Mapping):
        raise HardeningError("demo rule lock has an unsupported schema")
    locked_rules = dict(lock["rules"])
    locked_digest = str(lock.get("rulesSha256", ""))
    calculated_lock_digest = rules_digest(locked_rules)
    if locked_digest != calculated_lock_digest:
        raise HardeningError("demo rule lock digest does not match its frozen rules")
    if rules != locked_rules:
        raise HardeningError("active configuration does not match the frozen demo rules")

    _audit_logging(config)
    _audit_platform_sources(project_root)
    _audit_pac_template(project_root / "pac" / "demo-proxy.pac")
    result: dict[str, Any] = {
        "artifactVerified": False,
        "directFallbackConfigured": True,
        "liveVerified": False,
        "loopbackConfigured": config.proxy.listen_host == "127.0.0.1",
        "payloadLoggingDisabled": True,
        "rulesSha256": locked_digest,
        "status": "passed",
        "targetHost": config.target.host,
    }
    if artifact_path is not None:
        _audit_artifact(
            artifact_path=artifact_path,
            project_root=project_root,
            frozen_target=config.target.host,
        )
        result["artifactVerified"] = True
    if live:
        result["live"] = _audit_live(config)
        result["liveVerified"] = True
    return result


def frozen_rules(config: AppConfig) -> dict[str, Any]:
    """Return the normalized configuration surface locked for the demo."""

    return {
        "logging": {
            "logRequestBodies": config.logging.log_request_bodies,
            "logResponseBodies": config.logging.log_response_bodies,
            "redactHeaders": sorted(config.logging.redact_headers),
        },
        "matching": {
            "requiredRequestHeaders": dict(
                sorted(config.matching.required_request_headers.items())
            )
        },
        "platform": {
            "healthPort": config.platform.health_port,
            "pacPort": config.platform.pac_port,
        },
        "proxy": {
            "failOpen": config.proxy.fail_open,
            "listenHost": config.proxy.listen_host,
            "listenPort": config.proxy.listen_port,
            "maxBufferBytes": config.proxy.max_buffer_bytes,
        },
        "target": {
            "host": config.target.host,
            "methods": list(config.target.methods),
            "paths": list(config.target.paths),
            "port": config.target.port,
            "requestContentTypes": list(config.target.request_content_types),
            "responseContentTypes": list(config.target.response_content_types),
            "scheme": config.target.scheme,
        },
        "transformation": {
            "enabled": config.transformation.enabled,
            "mode": config.transformation.mode,
            "preserveUnknownFields": config.transformation.preserve_unknown_fields,
            "transformerVersion": config.transformation.transformer_version,
        },
    }


def rules_digest(rules: Mapping[str, Any]) -> str:
    canonical = json.dumps(
        rules, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def create_lock(config: AppConfig) -> dict[str, Any]:
    rules = frozen_rules(config)
    return {
        "formatVersion": 1,
        "rules": rules,
        "rulesSha256": rules_digest(rules),
    }


def _audit_logging(config: AppConfig) -> None:
    if config.logging.log_request_bodies or config.logging.log_response_bodies:
        raise HardeningError("payload logging must remain disabled")
    if not _REQUIRED_REDACTIONS.issubset(config.logging.redact_headers):
        raise HardeningError("required sensitive-header redactions are missing")
    if _FORBIDDEN_EVENT_FIELDS.intersection(EVENT_FIELDS):
        raise HardeningError("structured logging schema contains sensitive fields")
    if not config.proxy.fail_open:
        raise HardeningError("demo proxy must remain fail-open")


def _audit_platform_sources(project_root: Path) -> None:
    scripts_root = project_root / "scripts"
    for path in sorted(scripts_root.rglob("*")):
        if path.suffix not in {".ps1", ".sh"} or not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        matches = sorted(token for token in _FORBIDDEN_SCRIPT_TOKENS if token in content)
        if matches:
            raise HardeningError(f"unsafe platform mutation in {path}: {matches}")


def _audit_pac_template(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    if content.count("__TARGET_HOST__") != 1 or content.count("__PROXY_ENDPOINT__") != 1:
        raise HardeningError("PAC template must contain one exact target and proxy placeholder")
    if content.count('return "DIRECT";') != 1:
        raise HardeningError("PAC template must retain one unconditional DIRECT fallback")
    if content.count("PROXY __PROXY_ENDPOINT__; DIRECT") != 1:
        raise HardeningError("PAC target route must fail open to DIRECT")


def _audit_artifact(
    *, artifact_path: Path, project_root: Path, frozen_target: str
) -> None:
    names, read_bytes = _archive_reader(artifact_path)
    file_names = {
        name
        for name in names
        if not name.endswith("/")
        and not any(other.startswith(f"{name}/") for other in names if other != name)
    }
    for name in file_names:
        if any(fragment in name for fragment in _FORBIDDEN_ARCHIVE_FRAGMENTS):
            raise HardeningError(f"forbidden release content: {name}")
    manifest_name = _single_suffix(file_names, "/MANIFEST.json")
    config_name = _single_suffix(file_names, "/config/proxy.yaml")
    lock_name = _single_suffix(file_names, "/config/demo-lock.json")
    manifest = json.loads(read_bytes(manifest_name))
    manifest_files = manifest.get("files")
    if not isinstance(manifest_files, dict):
        raise HardeningError("release manifest file map is missing")
    prefix = manifest_name.removesuffix("MANIFEST.json")
    expected_files = {f"{prefix}{name}" for name in manifest_files}
    if expected_files.union({manifest_name}) != file_names:
        missing = sorted(expected_files.difference(file_names))
        extra = sorted(file_names.difference(expected_files.union({manifest_name})))
        raise HardeningError(
            f"release files do not exactly match MANIFEST.json; missing={missing}, extra={extra}"
        )
    for relative, expected_digest in manifest_files.items():
        actual = hashlib.sha256(read_bytes(f"{prefix}{relative}")).hexdigest()
        if actual != expected_digest:
            raise HardeningError(f"release manifest digest mismatch: {relative}")
    packaged_config = read_bytes(config_name)
    sanitized_config = (project_root / "config" / "proxy.example.yaml").read_bytes()
    if packaged_config != sanitized_config or frozen_target.encode() in packaged_config:
        raise HardeningError("release must contain only the sanitized configuration")
    packaged_lock = json.loads(read_bytes(lock_name))
    try:
        packaged_rules = frozen_rules(parse_config(yaml.safe_load(packaged_config)))
    except (ConfigError, yaml.YAMLError) as exc:
        raise HardeningError("packaged configuration is invalid") from exc
    if packaged_lock != {
        "formatVersion": 1,
        "rules": packaged_rules,
        "rulesSha256": rules_digest(packaged_rules),
    }:
        raise HardeningError("packaged rule lock does not match sanitized configuration")
    checksum_path = artifact_path.parent / "SHA256SUMS.txt"
    expected_line = f"{hashlib.sha256(artifact_path.read_bytes()).hexdigest()}  {artifact_path.name}"
    if expected_line not in checksum_path.read_text(encoding="ascii").splitlines():
        raise HardeningError("release checksum is missing or stale")


def _archive_reader(
    path: Path,
) -> tuple[set[str], Callable[[str], bytes]]:
    if path.name.endswith(".zip"):
        archive = zipfile.ZipFile(path)
        return set(archive.namelist()), archive.read
    if path.name.endswith(".tar.gz"):
        archive = tarfile.open(path, "r:gz")

        def read_bytes(name: str) -> bytes:
            extracted = archive.extractfile(name)
            if extracted is None:
                raise HardeningError(f"unable to read release member: {name}")
            return extracted.read()

        return set(archive.getnames()), read_bytes
    raise HardeningError(f"unsupported release artifact: {path}")


def _single_suffix(names: set[str], suffix: str) -> str:
    matches = [name for name in names if name.endswith(suffix)]
    if len(matches) != 1:
        raise HardeningError(f"release requires exactly one {suffix}")
    return matches[0]


def _audit_live(config: AppConfig) -> dict[str, Any]:
    ports = (
        config.proxy.listen_port,
        config.platform.health_port,
        config.platform.pac_port,
    )
    for port in ports:
        if not _connects("127.0.0.1", port):
            raise HardeningError(f"expected loopback listener is unavailable: {port}")
    non_loopback = _local_non_loopback_ip()
    if non_loopback:
        for port in ports:
            if _connects(non_loopback, port):
                raise HardeningError(
                    f"listener is reachable through non-loopback address {non_loopback}:{port}"
                )
    health = json.loads(
        _read_url(f"http://127.0.0.1:{config.platform.health_port}/health")
    )
    if health.get("status") != "ok" or health.get("targetHost") != config.target.host:
        raise HardeningError(f"live health is not demo-ready: {health}")
    pac = _read_url(
        f"http://127.0.0.1:{config.platform.pac_port}/demo-proxy.pac"
    )
    if config.target.host not in pac or pac.count('return "DIRECT";') != 1:
        raise HardeningError("live PAC does not retain exact target routing and DIRECT fallback")
    return {"nonLoopbackAddress": non_loopback, "ports": list(ports)}


def _connects(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def _local_non_loopback_ip() -> str | None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("192.0.2.1", 9))
        address = str(sock.getsockname()[0])
        return None if address.startswith("127.") else address
    except OSError:
        return None
    finally:
        sock.close()


def _read_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=2) as response:
        return response.read().decode("utf-8")


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HardeningError(f"unable to read {label}: {path}") from exc
    if not isinstance(value, dict):
        raise HardeningError(f"{label} must be a JSON object")
    return value
