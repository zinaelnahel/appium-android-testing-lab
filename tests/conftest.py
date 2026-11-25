import os
import re
from pathlib import Path

import pytest

from appium_framework.config import AppiumConfig
from appium_framework.driver import create_driver


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APK = ROOT / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
ARTIFACTS = Path(os.getenv("APPIUM_ARTIFACTS_DIR", ROOT / "artifacts")).expanduser()
if not ARTIFACTS.is_absolute():
    ARTIFACTS = ROOT / ARTIFACTS


@pytest.fixture
def driver():
    config = AppiumConfig.from_env(default_app=DEFAULT_APK)
    session = create_driver(config)
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

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)
    try:
        session.save_screenshot(str(ARTIFACTS / f"{safe_name}.png"))
    except Exception:
        pass
    try:
        (ARTIFACTS / f"{safe_name}.page-source.txt").write_text(
            session.page_source, encoding="utf-8"
        )
    except Exception:
        pass
