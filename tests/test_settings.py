from tests.screen_objects import HomeScreen, LoginScreen, SettingsScreen


def test_notification_preference_can_be_enabled(driver):
    LoginScreen(driver).sign_in("demo@example.com", "QualityLab123!")
    HomeScreen(driver).open_settings()
    settings = SettingsScreen(driver)

    assert settings.text("notifications-status") == "Notifications are off."

    settings.toggle_notifications()

    assert settings.text("notifications-status") == "Notifications are on."
