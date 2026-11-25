from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait


class Screen:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def element(self, accessibility_id):
        return self.wait.until(
            conditions.visibility_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, accessibility_id)
            )
        )

    def tap(self, accessibility_id):
        self.element(accessibility_id).click()

    def text(self, accessibility_id):
        return self.element(accessibility_id).text


class LoginScreen(Screen):
    def sign_in(self, email, password):
        self.element("login-email").send_keys(email)
        self.element("login-password").send_keys(password)
        self.tap("login-submit")


class HomeScreen(Screen):
    def open_search(self):
        self.tap("home-search")

    def open_settings(self):
        self.tap("home-settings")


class SearchScreen(Screen):
    def search_for(self, query):
        self.element("search-query").send_keys(query)
        self.tap("search-submit")


class SettingsScreen(Screen):
    def toggle_notifications(self):
        self.tap("settings-notifications-toggle")
