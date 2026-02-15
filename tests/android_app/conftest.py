import os
import json
import logging

import pytest
import allure
from selene import browser
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config import load_config

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def mobile_management():
    config = load_config()

    if config["context"] in ["local_emulator", "local_real"]:
        package = config["appPackage"]
        os.system(f"adb -s {config['udid']} shell pm clear {package}")

    if config["context"] == "bstack":
        driver = create_bstack_driver(config)
    else:
        driver = create_local_driver(config)

    browser.config.driver = driver
    browser.config.timeout = config["timeout"]

    yield driver

    # --- Allure attachments ---
    attach_screenshot()
    attach_page_source()
    attach_capabilities()
    attach_video()

    driver.quit()
    browser.config.driver = None


def create_bstack_driver(config):
    options = UiAutomator2Options().load_capabilities({
        "platformName": config["platformName"],
        "platformVersion": config["platformVersion"],
        "deviceName": config["deviceName"],

        "app": config["bstack"]["app"],

        "bstack:options": {
            "projectName": config["bstack"]["project"],
            "buildName": config["bstack"]["build"],
            "sessionName": config["bstack"]["session"],
            "userName": config["bstack"]["user"],
            "accessKey": config["bstack"]["key"]
        }
    })

    return webdriver.Remote(
        command_executor=config["appium_server_url"],
        options=options
    )


def create_local_driver(config):
    options = UiAutomator2Options().load_capabilities({
        "platformName": config["platformName"],
        "platformVersion": config["platformVersion"],
        "deviceName": config["deviceName"],
        "udid": config["udid"],
        "appPackage": config["appPackage"],
        "appActivity": config["appActivity"],
        "noReset": True,
        "autoGrantPermissions": True,
    })

    return webdriver.Remote(
        command_executor=config["appium_server_url"],
        options=options
    )


def attach_screenshot():
    try:
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        logger.warning(f"Failed to attach screenshot: {e}")


def attach_page_source():
    try:
        allure.attach(
            browser.driver.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.XML
        )
    except Exception as e:
        logger.warning(f"Failed to attach page source: {e}")


def attach_capabilities():
    try:
        caps = json.dumps(browser.driver.capabilities, indent=4)
        allure.attach(
            caps,
            name="capabilities",
            attachment_type=allure.attachment_type.JSON
        )
    except Exception as e:
        logger.warning(f"Failed to attach capabilities: {e}")


def attach_video():
    try:
        session_id = browser.driver.session_id
        video_url = f"https://app-automate.browserstack.com/sessions/{session_id}.json"
        allure.attach(
            video_url,
            name="video",
            attachment_type=allure.attachment_type.URI_LIST
        )
    except Exception as e:
        logger.warning(f"Failed to attach video URL: {e}")
