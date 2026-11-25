# Appium Mobile Testing Framework

[![Android E2E](https://github.com/zinaelnahel/appium-android-testing-lab/actions/workflows/android-e2e.yml/badge.svg)](https://github.com/zinaelnahel/appium-android-testing-lab/actions/workflows/android-e2e.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Appium](https://img.shields.io/badge/Appium-Python%20Client-663399?logo=appium&logoColor=white)
![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

A reusable **Appium + Python + pytest** framework for building mobile UI automation suites. It includes a small Android sample app so the framework has a real target, example page objects, end-to-end scenarios, and a GitHub Actions run with downloadable test evidence.

> The framework handles Appium session setup, common UI helpers, and failure evidence. You still write app-specific page objects and test cases for each app—there is no one-size-fits-all test suite.

## What this project demonstrates

- Creating isolated Appium sessions from environment-based capabilities
- Running against Android or iOS by selecting the matching Appium driver
- Organizing app-specific UI automation with page objects and pytest fixtures
- Using accessibility IDs and explicit waits for stable interactions
- Capturing screenshots and page source when a test fails
- Running a real Android sample suite in GitHub Actions and retaining CI evidence

## Architecture

```text
appium_framework/
  config.py              Environment-based Appium capabilities
  driver.py              Appium session factory
  screen.py              Reusable explicit-wait and interaction helpers
tests/
  conftest.py            Driver lifecycle and failure evidence
  screen_objects.py      QualityLab sample app page objects
  test_login.py          Example login scenarios
  test_search.py         Example search scenario
  test_settings.py       Example settings scenario
app/                     Small native Android sample app under test
.github/workflows/       Android emulator CI workflow
```

## Included sample app: QualityLab

QualityLab is intentionally small; it demonstrates how to structure tests without tying the framework to one product.

| Flow | Example checks |
| --- | --- |
| Login | Valid credentials open the home screen; invalid credentials show an error |
| Search | A query returns a matching result |
| Settings | The notification preference can be enabled |

Demo credentials: `demo@example.com` / `QualityLab123!`

## Run the sample locally

Requirements: Python 3.10+, JDK 17, Android SDK and emulator, Gradle, Node.js/npm.

1. Build the sample APK:

   ```bash
   gradle --no-daemon assembleDebug
   ```

2. Install Python and Appium dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   npm install --global appium
   appium driver install uiautomator2
   ```

3. Start an Android emulator. In a separate terminal, start the server and run the tests:

   ```bash
   appium
   ```

   ```bash
   cp .env.example .env
   set -a && source .env && set +a
   pytest -q
   ```

The sample APK path is the default. Override `APPIUM_APP` if you build or store it elsewhere.

## Use the framework with your app

1. Install the Appium driver for your target platform: `uiautomator2` for Android or `xcuitest` for iOS.
2. Copy `.env.example` and set the server URL, platform, device, and app capability. Use `APPIUM_APP` for an APK, app bundle, or provider app reference. For an already-installed app, set its package/activity (Android) or bundle ID (iOS) in `APPIUM_EXTRA_CAPS`.
3. Add page objects and tests that reflect your app's screens and expected behavior. Start from `tests/screen_objects.py` and the three sample test files.
4. Run with `pytest -q`. For a cloud device provider, point `APPIUM_SERVER_URL` to its Appium endpoint and add provider-specific capabilities in `APPIUM_EXTRA_CAPS`.

Use accessibility IDs or other stable app identifiers wherever possible. Inspect the app with Appium Inspector and ask the app team to add accessibility identifiers when the UI does not expose reliable selectors.

### Platform notes

- **Android:** the included GitHub Actions workflow builds QualityLab, starts an Android emulator, and runs the sample tests on every push and pull request.
- **iOS:** the session factory selects XCUITest when `APPIUM_PLATFORM=iOS`. iOS execution requires macOS with Xcode and the XCUITest driver; this repository's CI currently demonstrates Android only.

## Capabilities

The driver reads these environment variables:

| Variable | Purpose |
| --- | --- |
| `APPIUM_SERVER_URL` | Local or cloud Appium server URL |
| `APPIUM_PLATFORM` | `Android` (default) or `iOS` |
| `APPIUM_AUTOMATION_NAME` | Optional override; defaults to UiAutomator2 or XCUITest |
| `APPIUM_DEVICE_NAME` | Target device name |
| `APPIUM_PLATFORM_VERSION` | Optional OS version |
| `APPIUM_APP` | APK/app path or remote provider app reference |
| `APPIUM_APP_PACKAGE` | Optional Android package for an already-installed app |
| `APPIUM_APP_ACTIVITY` | Optional Android activity for an already-installed app |
| `APPIUM_NO_RESET` | Preserve app data between sessions (`false` by default) |
| `APPIUM_AUTO_GRANT_PERMISSIONS` | Automatically grant Android permissions (`true` by default) |
| `APPIUM_EXTRA_CAPS` | JSON object merged into capabilities for platform/provider options |

See `.env.example` for a ready-to-copy configuration.

## CI evidence

Open **Actions → Android E2E** to see the emulator run. Each run uploads an `android-e2e-evidence` artifact containing the JUnit report, Appium logs, and Android logcat. Failed tests also save screenshots and the UI page source. The same workflow runs on pushes and pull requests.

## Portfolio walkthrough

When presenting the project, highlight the reusable driver configuration, the screen-object pattern, synchronization through explicit waits, and how CI preserves failure evidence. The sample app is there to make those techniques runnable and reviewable.
