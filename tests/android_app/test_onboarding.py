import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from helpers.onboarding import onboarding_present, get_text


def test_onboarding(mobile_management):
    driver = mobile_management
    package = driver.capabilities["appPackage"]

    if not onboarding_present(driver, package):
        pytest.skip("Onboarding is not shown on this device")

    skip_btns = driver.find_elements(AppiumBy.ID, f"{package}:id/fragment_onboarding_skip_button")
    if skip_btns:
        skip_btns[0].click()
    else:
        text1 = get_text(driver, package)
        assert "The Free Encyclopedia" in text1 or "Свободная энциклопедия" in text1
        driver.find_element(AppiumBy.ID, f"{package}:id/fragment_onboarding_forward_button").click()

        time.sleep(1)
        text2 = get_text(driver, package)
        assert "New ways to explore" in text2 or "Мы нашли следующие языки" in text2
        driver.find_element(AppiumBy.ID, f"{package}:id/fragment_onboarding_forward_button").click()

        time.sleep(1)
        text3 = get_text(driver, package)
        assert "Reading lists with sync" in text3 or "Русский" in text3
        driver.find_element(AppiumBy.ID, f"{package}:id/fragment_onboarding_forward_button").click()

        time.sleep(1)
        text4 = get_text(driver, package)
        assert "Data & Privacy" in text4 or "Добавить или удалить язык" in text4
        driver.find_element(AppiumBy.ID, f"{package}:id/fragment_onboarding_done_button").click()

    home = driver.find_elements(AppiumBy.ID, f"{package}:id/main_toolbar_wordmark")
    assert home, "Home screen did not appear after onboarding"