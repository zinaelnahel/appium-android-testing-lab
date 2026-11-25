from tests.screen_objects import LoginScreen


def test_valid_login_opens_home_screen(driver):
    LoginScreen(driver).sign_in("demo@example.com", "QualityLab123!")

    assert driver.find_element("accessibility id", "screen-title").text == "Welcome, Demo Tester"


def test_invalid_login_shows_actionable_error(driver):
    login = LoginScreen(driver)
    login.sign_in("demo@example.com", "wrong-password")

    assert login.text("login-error") == "Email or password is incorrect."
