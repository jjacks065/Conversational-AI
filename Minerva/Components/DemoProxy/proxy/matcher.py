"""Strict response eligibility matching independent of mitmproxy internals."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlsplit

from .config import AppConfig, normalize_media_type


@dataclass(frozen=True)
class RequestMetadata:
    scheme: str
    host: str
    port: int
    method: str
    path: str
    headers: Mapping[str, str]


@dataclass(frozen=True)
class ResponseMetadata:
    headers: Mapping[str, str]


@dataclass(frozen=True)
class MatchDecision:
    matched: bool
    reason: str
    path_pattern: str | None = None


class ResponseMatcher:
    """Evaluate every configured request and response condition."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._path_patterns = tuple(re.compile(value) for value in config.target.paths)
        self._header_patterns = {
            name: re.compile(value)
            for name, value in config.matching.required_request_headers.items()
        }

    def evaluate(
        self, request: RequestMetadata, response: ResponseMetadata
    ) -> MatchDecision:
        if not self._config.transformation.enabled:
            return MatchDecision(False, "transformation_disabled")
        if request.scheme.lower() != self._config.target.scheme:
            return MatchDecision(False, "scheme")
        if request.host.lower() != self._config.target.host:
            return MatchDecision(False, "host")
        if request.port != self._config.target.port:
            return MatchDecision(False, "port")
        if request.method.upper() not in self._config.target.methods:
            return MatchDecision(False, "method")

        request_path = urlsplit(request.path).path
        path_pattern = next(
            (pattern for pattern in self._path_patterns if pattern.fullmatch(request_path)),
            None,
        )
        if path_pattern is None:
            return MatchDecision(False, "path")

        request_headers = _casefold_headers(request.headers)
        response_headers = _casefold_headers(response.headers)
        if not _media_type_allowed(
            request_headers.get("content-type"),
            self._config.target.request_content_types,
        ):
            return MatchDecision(False, "request_content_type")
        if not _media_type_allowed(
            response_headers.get("content-type"),
            self._config.target.response_content_types,
        ):
            return MatchDecision(False, "response_content_type")

        for name, pattern in self._header_patterns.items():
            value = request_headers.get(name)
            if value is None:
                return MatchDecision(False, "required_header_missing")
            if pattern.fullmatch(value) is None:
                return MatchDecision(False, "required_header_mismatch")

        return MatchDecision(True, "matched", path_pattern.pattern)


def _casefold_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {str(name).lower(): str(value) for name, value in headers.items()}


def _media_type_allowed(value: str | None, allowlist: tuple[str, ...]) -> bool:
    if value is None:
        return False
    try:
        return normalize_media_type(value) in allowlist
    except ValueError:
        return False
