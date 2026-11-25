from appium import webdriver
from appium.options.common import AppiumOptions

from appium_framework.config import AppiumConfig


def create_driver(config: AppiumConfig):
    """Create an Appium session using the supplied platform capabilities."""
    options = AppiumOptions()
    for name, value in config.capabilities().items():
        options.set_capability(name, value)
    return webdriver.Remote(config.server_url, options=options)
