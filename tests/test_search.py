from tests.screen_objects import HomeScreen, LoginScreen, SearchScreen


def test_accessibility_search_returns_relevant_result(driver):
    LoginScreen(driver).sign_in("demo@example.com", "QualityLab123!")
    HomeScreen(driver).open_search()
    SearchScreen(driver).search_for("accessibility")

    assert "Accessibility checklist" in SearchScreen(driver).text("search-result")
