from __future__ import annotations

import copy
import unittest
from pathlib import Path

from proxy.config import ConfigError, load_config, parse_config


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "proxy.yaml"


def valid_config_mapping() -> dict[str, object]:
    return {
        "proxy": {
            "listen_host": "127.0.0.1",
            "listen_port": 8080,
            "fail_open": True,
            "max_buffer_bytes": 10_485_760,
        },
        "target": {
            "scheme": "https",
            "host": "api.example.com",
            "port": 443,
            "methods": ["post"],
            "paths": [r"^/api/chatbot/ask$"],
            "request_content_types": ["Application/JSON; Charset=UTF-8"],
            "response_content_types": ["application/json"],
        },
        "matching": {
            "required_request_headers": {
                "Origin": r"^https://demo\.example\.com$",
            }
        },
        "transformation": {
            "enabled": True,
            "mode": "deterministic",
            "preserve_unknown_fields": True,
            "transformer_version": "1.0.0",
        },
        "logging": {
            "level": "info",
            "log_request_bodies": False,
            "log_response_bodies": False,
            "log_match_decisions": True,
            "redact_headers": ["Authorization", "Cookie", "Set-Cookie"],
        },
        "platform": {
            "browser_profile_name": "DemoProxyProfile",
            "health_port": 8081,
            "pac_port": 8765,
        },
    }


class ConfigTests(unittest.TestCase):
    def test_loads_real_configuration_and_normalizes_match_values(self) -> None:
        config = load_config(CONFIG_PATH)

        self.assertEqual(
            config.target.host,
            "app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net",
        )
        self.assertEqual(config.target.methods, ("POST",))
        self.assertEqual(config.target.request_content_types, ("application/json",))
        self.assertEqual(config.matching.required_request_headers.keys(), {"origin"})
        self.assertEqual(config.proxy.listen_host, "127.0.0.1")
        self.assertEqual(config.platform.health_port, 8081)
        self.assertEqual(config.platform.pac_port, 8765)

    def test_parse_does_not_mutate_source_mapping(self) -> None:
        source = valid_config_mapping()
        original = copy.deepcopy(source)

        parse_config(source)

        self.assertEqual(source, original)

    def test_normalizes_methods_media_types_header_names_and_log_level(self) -> None:
        config = parse_config(valid_config_mapping())

        self.assertEqual(config.target.methods, ("POST",))
        self.assertEqual(config.target.request_content_types, ("application/json",))
        self.assertEqual(config.matching.required_request_headers.keys(), {"origin"})
        self.assertEqual(config.logging.level, "INFO")
        self.assertEqual(
            config.logging.redact_headers,
            frozenset({"authorization", "cookie", "set-cookie"}),
        )

    def test_rejects_non_loopback_proxy_listener(self) -> None:
        source = valid_config_mapping()
        source["proxy"]["listen_host"] = "0.0.0.0"  # type: ignore[index]

        with self.assertRaisesRegex(ConfigError, "loopback"):
            parse_config(source)

    def test_rejects_body_logging(self) -> None:
        for key in ("log_request_bodies", "log_response_bodies"):
            source = valid_config_mapping()
            source["logging"][key] = True  # type: ignore[index]
            with self.subTest(key=key):
                with self.assertRaisesRegex(ConfigError, "must be false"):
                    parse_config(source)

    def test_rejects_invalid_path_or_header_regex(self) -> None:
        path_source = valid_config_mapping()
        path_source["target"]["paths"] = ["["]  # type: ignore[index]
        header_source = valid_config_mapping()
        header_source["matching"]["required_request_headers"] = {  # type: ignore[index]
            "origin": "["
        }

        for source in (path_source, header_source):
            with self.subTest(source=source):
                with self.assertRaisesRegex(ConfigError, "regular expression"):
                    parse_config(source)

    def test_rejects_unknown_keys_and_missing_sections(self) -> None:
        unknown = valid_config_mapping()
        unknown["proxy"]["surprise"] = True  # type: ignore[index]
        missing = valid_config_mapping()
        del missing["target"]

        with self.assertRaisesRegex(ConfigError, "unknown key"):
            parse_config(unknown)
        with self.assertRaisesRegex(ConfigError, "missing section: target"):
            parse_config(missing)

    def test_rejects_invalid_ports_and_empty_allowlists(self) -> None:
        invalid_port = valid_config_mapping()
        invalid_port["proxy"]["listen_port"] = 70_000  # type: ignore[index]
        empty_methods = valid_config_mapping()
        empty_methods["target"]["methods"] = []  # type: ignore[index]

        with self.assertRaisesRegex(ConfigError, "listen_port"):
            parse_config(invalid_port)
        with self.assertRaisesRegex(ConfigError, "methods"):
            parse_config(empty_methods)

    def test_rejects_colliding_service_ports(self) -> None:
        source = valid_config_mapping()
        source["platform"]["pac_port"] = 8081  # type: ignore[index]

        with self.assertRaisesRegex(ConfigError, "must be distinct"):
            parse_config(source)


if __name__ == "__main__":
    unittest.main()
