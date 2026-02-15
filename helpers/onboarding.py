from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import time
import logging

logger = logging.getLogger(__name__)


def onboarding_present(driver, package):
    elements = driver.find_elements(AppiumBy.ID, f"{package}:id/fragment_onboarding_skip_button")
    if elements:
        return True

    elements = driver.find_elements(AppiumBy.ID, f"{package}:id/primaryTextView")
    if elements:
        return True

    logger.info("Onboarding not found on this device")
    return False


def get_text(driver, package):
    for _ in range(3):
        elements = driver.find_elements(AppiumBy.ID, f"{package}:id/primaryTextView")
        if elements:
            return elements[0].text
        time.sleep(0.5)

    logger.warning("Failed to get onboarding text after retries")
    return ""
