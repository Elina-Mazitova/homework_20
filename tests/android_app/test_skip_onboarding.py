from helpers.onboarding import onboarding_present
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy



def test_onboarding_skip(mobile_management):
    driver = mobile_management
    package = driver.capabilities["appPackage"]

    if not onboarding_present(driver, package):
        pytest.skip("Onboarding is not shown on this device")

    skip_btns = driver.find_elements(AppiumBy.ID, f"{package}:id/fragment_onboarding_skip_button")
    assert skip_btns, "Skip button is not shown on onboarding"

    skip_btns[0].click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((AppiumBy.ID, f"{package}:id/main_toolbar_wordmark"))
    )
