# Appium Android Testing Lab

[![Android E2E](https://github.com/zinaelnahel/appium-android-testing-lab/actions/workflows/android-e2e.yml/badge.svg)](https://github.com/zinaelnahel/appium-android-testing-lab/actions/workflows/android-e2e.yml)

A small native Android app built to demonstrate reliable mobile UI testing with **Appium, Python, and pytest**. The suite exercises real user flows on an Android emulator in GitHub Actions and keeps useful failure evidence.

## What this demonstrates

- Android end-to-end tests with Appium's **UiAutomator2** driver
- Python test organization with pytest fixtures and screen objects
- Stable accessibility ID selectors and explicit waits
- Isolated test sessions with deterministic demo data
- CI execution on an Android emulator for pushes and pull requests
- Failure artifacts: screenshots, page source, JUnit XML, Appium logs, and Android logcat

## App under test

**QualityLab** is an intentionally small app with three testable flows:

| Flow | Example checks |
| --- | --- |
| Login | Valid credentials reach the home screen; invalid credentials show a clear error |
| Search | A search query returns a matching result |
| Settings | Notification preference changes from off to on |

Demo credentials: `demo@example.com` / `QualityLab123!`

The app exposes stable accessibility IDs such as `login-email`, `login-submit`, and `search-query`. The tests use those IDs instead of brittle XPath or screen coordinates.

## Test layout

```text
app/                         Native Android app under test
tests/
  conftest.py                Appium session and failure evidence
  screen_objects.py          Small screen objects and explicit waits
  test_login.py
  test_search.py
  test_settings.py
.github/workflows/
  android-e2e.yml            Build, emulator, Appium, pytest, artifacts
```

## Run locally

Requirements: JDK 17, Android SDK with an API 35 emulator, Gradle 9.6, Node.js/npm, and Python 3.11+.

1. Build the demo app:

   ```bash
   gradle assembleDebug
   ```

2. Install Python dependencies and Appium:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   npm install --global appium
   appium driver install uiautomator2
   ```

3. Start an API 35 Android emulator, then start the Appium server in another terminal:

   ```bash
   appium
   ```

4. Run the suite:

   ```bash
   export APPIUM_APP="$PWD/app/build/outputs/apk/debug/app-debug.apk"
   pytest -q
   ```

The server URL defaults to `http://127.0.0.1:4723`. Set `APPIUM_SERVER_URL` to use another local endpoint.

## CI and failure evidence

The workflow builds the app, starts an API 35 emulator, installs the UiAutomator2 driver, and runs the same pytest suite. On failure, the tests capture a screenshot and page source for the failing session. The workflow also saves the Appium server log, Android logcat, and JUnit report as a downloadable artifact.

Open **Actions → Android E2E** to see each run. No cloud device account, paid service, or private test credential is needed.

## Design choices

- **Accessibility IDs:** selectors stay readable and less sensitive to layout changes.
- **Explicit waits:** the suite waits for UI state instead of sleeping for fixed durations.
- **Fresh Appium session per test:** test state does not leak between scenarios.
- **Useful failure context:** screenshots and page source help explain what the test saw.

This first version targets Android. iOS can be added later with the XCUITest driver and a macOS runner.
