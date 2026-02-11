from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import time
import pytest


def onboarding_present(driver, package):
    try:
        driver.find_element(AppiumBy.ID, f"{package}:id/fragment_onboarding_skip_button")
        return True
    except NoSuchElementException:
        pass

    try:
        driver.find_element(AppiumBy.ID, f"{package}:id/primaryTextView")
        return True
    except NoSuchElementException:
        pass

    return False


def get_text(driver, package):
    for _ in range(3):
        try:
            return driver.find_element(AppiumBy.ID, f"{package}:id/primaryTextView").text
        except Exception:
            time.sleep(0.5)
    return ""


def test_onboarding(mobile_management):
    driver = mobile_management

    package = driver.capabilities["appPackage"]

    if not onboarding_present(driver, package):
        pytest.skip("Onboarding is not shown on this device")

    # Русский онбординг (кнопка Пропустить)
    try:
        skip_btn = driver.find_element(AppiumBy.ID, f"{package}:id/fragment_onboarding_skip_button")
        skip_btn.click()
        return
    except NoSuchElementException:
        pass

    #Английский онбординг
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
