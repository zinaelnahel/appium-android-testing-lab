from tests.screen_objects import HomeScreen, LoginScreen


def test_valid_login_opens_home_screen(driver):
    LoginScreen(driver).sign_in("demo@example.com", "QualityLab123!")

    assert HomeScreen(driver).title == "Welcome, Demo Tester"


def test_invalid_login_shows_actionable_error(driver):
    login = LoginScreen(driver)
    login.sign_in("demo@example.com", "wrong-password")

    assert login.error_message == "Email or password is incorrect."
