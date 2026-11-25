from appium.webdriver.common.appiumby import AppiumBy

from appium_framework.screen import BaseScreen


class LoginScreen(BaseScreen):
    EMAIL = (AppiumBy.ACCESSIBILITY_ID, "login-email")
    PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "login-password")
    SUBMIT = (AppiumBy.ACCESSIBILITY_ID, "login-submit")
    ERROR = (AppiumBy.ACCESSIBILITY_ID, "login-error")

    def sign_in(self, email, password):
        self.enter_text(self.EMAIL, email)
        self.enter_text(self.PASSWORD, password)
        self.tap(self.SUBMIT)

    @property
    def error_message(self):
        return self.text(self.ERROR)


class HomeScreen(BaseScreen):
    TITLE = (AppiumBy.ACCESSIBILITY_ID, "screen-title")
    SEARCH = (AppiumBy.ACCESSIBILITY_ID, "home-search")
    SETTINGS = (AppiumBy.ACCESSIBILITY_ID, "home-settings")

    @property
    def title(self):
        return self.text(self.TITLE)

    def open_search(self):
        self.tap(self.SEARCH)

    def open_settings(self):
        self.tap(self.SETTINGS)


class SearchScreen(BaseScreen):
    QUERY = (AppiumBy.ACCESSIBILITY_ID, "search-query")
    SUBMIT = (AppiumBy.ACCESSIBILITY_ID, "search-submit")
    RESULT = (AppiumBy.ACCESSIBILITY_ID, "search-result")

    def search_for(self, query):
        self.enter_text(self.QUERY, query)
        self.tap(self.SUBMIT)

    @property
    def result_text(self):
        return self.text(self.RESULT)


class SettingsScreen(BaseScreen):
    STATUS = (AppiumBy.ACCESSIBILITY_ID, "notifications-status")
    NOTIFICATIONS_TOGGLE = (
        AppiumBy.ACCESSIBILITY_ID,
        "settings-notifications-toggle",
    )

    @property
    def notifications_status(self):
        return self.text(self.STATUS)

    def toggle_notifications(self):
        self.tap(self.NOTIFICATIONS_TOGGLE)
