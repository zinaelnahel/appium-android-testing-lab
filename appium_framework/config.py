import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _boolean(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value, received {value!r}")


def _optional(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


@dataclass(frozen=True)
class AppiumConfig:
    server_url: str
    platform: str
    automation_name: str
    device_name: str
    platform_version: str | None = None
    app: str | None = None
    app_package: str | None = None
    app_activity: str | None = None
    no_reset: bool = False
    auto_grant_permissions: bool = True
    new_command_timeout: int = 120
    extra_capabilities: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls, default_app: Path | None = None) -> "AppiumConfig":
        platform = os.getenv("APPIUM_PLATFORM", "Android").strip()
        normalized_platform = platform.lower()
        if normalized_platform not in {"android", "ios"}:
            raise ValueError("APPIUM_PLATFORM must be Android or iOS")

        platform_name = "Android" if normalized_platform == "android" else "iOS"
        default_automation = (
            "UiAutomator2" if platform_name == "Android" else "XCUITest"
        )
        automation_name = os.getenv(
            "APPIUM_AUTOMATION_NAME", default_automation
        ).strip()

        app_value = _optional("APPIUM_APP")
        if app_value:
            candidate = Path(app_value).expanduser()
            app = str(candidate.resolve()) if candidate.exists() else app_value
        elif default_app and default_app.is_file():
            app = str(default_app.resolve())
        else:
            app = None

        extra_raw = os.getenv("APPIUM_EXTRA_CAPS", "{}")
        try:
            extra_capabilities = json.loads(extra_raw)
        except json.JSONDecodeError as error:
            raise ValueError("APPIUM_EXTRA_CAPS must be a valid JSON object") from error
        if not isinstance(extra_capabilities, dict):
            raise ValueError("APPIUM_EXTRA_CAPS must be a JSON object")

        try:
            new_command_timeout = int(os.getenv("APPIUM_NEW_COMMAND_TIMEOUT", "120"))
        except ValueError as error:
            raise ValueError("APPIUM_NEW_COMMAND_TIMEOUT must be an integer") from error

        config = cls(
            server_url=os.getenv(
                "APPIUM_SERVER_URL", "http://127.0.0.1:4723"
            ).rstrip("/"),
            platform=platform_name,
            automation_name=automation_name,
            device_name=os.getenv(
                "APPIUM_DEVICE_NAME",
                "Android Emulator" if platform_name == "Android" else "iPhone Simulator",
            ),
            platform_version=_optional("APPIUM_PLATFORM_VERSION"),
            app=app,
            app_package=_optional("APPIUM_APP_PACKAGE"),
            app_activity=_optional("APPIUM_APP_ACTIVITY"),
            no_reset=_boolean("APPIUM_NO_RESET", False),
            auto_grant_permissions=_boolean(
                "APPIUM_AUTO_GRANT_PERMISSIONS", True
            ),
            new_command_timeout=new_command_timeout,
            extra_capabilities=extra_capabilities,
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.server_url:
            raise ValueError("APPIUM_SERVER_URL cannot be empty")
        if not self.device_name:
            raise ValueError("APPIUM_DEVICE_NAME cannot be empty")
        if not self.automation_name:
            raise ValueError("APPIUM_AUTOMATION_NAME cannot be empty")
        if not self.app and not self.app_package:
            raise ValueError(
                "Set APPIUM_APP to an app path/reference, or set "
                "APPIUM_APP_PACKAGE for an already-installed app."
            )

    def capabilities(self) -> dict[str, Any]:
        capabilities: dict[str, Any] = {
            "platformName": self.platform,
            "appium:automationName": self.automation_name,
            "appium:deviceName": self.device_name,
            "appium:noReset": self.no_reset,
            "appium:newCommandTimeout": self.new_command_timeout,
        }
        if self.platform_version:
            capabilities["appium:platformVersion"] = self.platform_version
        if self.app:
            capabilities["appium:app"] = self.app
        if self.app_package:
            capabilities["appium:appPackage"] = self.app_package
        if self.app_activity:
            capabilities["appium:appActivity"] = self.app_activity
        if self.platform == "Android":
            capabilities["appium:autoGrantPermissions"] = (
                self.auto_grant_permissions
            )
        capabilities.update(self.extra_capabilities)
        return capabilities
