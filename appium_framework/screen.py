from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait


class BaseScreen:
    """Shared explicit-wait and interaction helpers for app-specific screens."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def element(self, locator):
        return self.wait.until(conditions.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(conditions.element_to_be_clickable(locator))

    def tap(self, locator):
        self.clickable(locator).click()

    def enter_text(self, locator, value: str, clear: bool = True):
        field = self.element(locator)
        if clear:
            field.clear()
        field.send_keys(value)

    def text(self, locator) -> str:
        return self.element(locator).text

    def is_visible(self, locator) -> bool:
        try:
            self.element(locator)
            return True
        except TimeoutException:
            return False
