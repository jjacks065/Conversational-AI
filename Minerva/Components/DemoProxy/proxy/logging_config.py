"""Structured metadata-only logging for the shared proxy."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime


EVENT_FIELDS = frozenset(
    {
        "timestamp",
        "platform",
        "proxy_version",
        "correlation_id",
        "match_result",
        "method",
        "host",
        "path_template",
        "status_code",
        "content_type",
        "transformation_duration_ms",
        "original_bytes",
        "transformed_bytes",
        "fail_open",
        "exception_category",
    }
)


class StructuredLogger:
    """Emit a fixed-schema JSON event that cannot accept bodies or headers."""

    def __init__(
        self,
        *,
        level: str,
        platform_label: str,
        proxy_version: str,
        logger: logging.Logger | None = None,
    ) -> None:
        self._platform_label = platform_label
        self._proxy_version = proxy_version
        self._logger = logger or logging.getLogger("demo_response_proxy")
        self._logger.setLevel(level.upper())
        if logger is None and not self._logger.handlers:
            self._logger.addHandler(logging.StreamHandler())

    def emit(
        self,
        *,
        correlation_id: str,
        match_result: str,
        method: str,
        host: str,
        path_template: str | None,
        status_code: int,
        content_type: str,
        transformation_duration_ms: float,
        original_bytes: int,
        transformed_bytes: int,
        fail_open: bool,
        exception_category: str | None,
    ) -> None:
        event = {
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "platform": self._platform_label,
            "proxy_version": self._proxy_version,
            "correlation_id": correlation_id,
            "match_result": match_result,
            "method": method,
            "host": host,
            "path_template": path_template,
            "status_code": status_code,
            "content_type": content_type,
            "transformation_duration_ms": round(transformation_duration_ms, 3),
            "original_bytes": original_bytes,
            "transformed_bytes": transformed_bytes,
            "fail_open": fail_open,
            "exception_category": exception_category,
        }
        self._logger.info(
            json.dumps(event, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        )
