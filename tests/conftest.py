import os
import re
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APK = ROOT / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
ARTIFACTS = ROOT / "artifacts"


@pytest.fixture
def driver():
    apk_path = Path(os.getenv("APPIUM_APP", str(DEFAULT_APK))).expanduser().resolve()
    if not apk_path.is_file():
        raise pytest.UsageError(
            "APK not found. Build it with 'gradle assembleDebug' or set APPIUM_APP "
            "to the debug APK path."
        )

    options = UiAutomator2Options().load_capabilities(
        {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
            "app": str(apk_path),
            "autoGrantPermissions": True,
            "newCommandTimeout": 120,
        }
    )
    server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    session = webdriver.Remote(server_url, options=options)
    yield session
    session.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    session = item.funcargs.get("driver")
    if session is None:
        return

    ARTIFACTS.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)
    try:
        session.save_screenshot(str(ARTIFACTS / f"{safe_name}.png"))
    except Exception:
        pass
    try:
        (ARTIFACTS / f"{safe_name}.xml").write_text(session.page_source, encoding="utf-8")
    except Exception:
        pass
