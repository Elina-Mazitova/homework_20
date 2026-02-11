from dotenv import load_dotenv
import os


def load_config():
    # Загружаем базовые .env
    load_dotenv(".env")
    load_dotenv(".env.credentials")

    # Читаем context
    context = os.getenv("context", "local_emulator")

    # Загружаем .env.<context>
    env_file = f".env.{context}"
    load_dotenv(env_file)

    # DEBUG
    print("\n=== CONFIG DEBUG ===")
    print(f"Loaded context: {context}")
    print(f"Loaded env file: {env_file}")
    print(f"UDID = {os.getenv('UDID')}")
    print(f"DeviceName = {os.getenv('DEVICE_NAME')}")
    print(f"Platform = {os.getenv('PLATFORM_NAME')}")
    print("====================\n")

    return {
        "context": context,
        "appium_server_url": os.getenv("APPIUM_SERVER_URL"),
        "platformName": os.getenv("PLATFORM_NAME"),
        "platformVersion": os.getenv("PLATFORM_VERSION"),
        "deviceName": os.getenv("DEVICE_NAME"),
        "udid": os.getenv("UDID"),

        # Универсальные параметры приложения
        "appPackage": os.getenv("APP_PACKAGE"),
        "appActivity": os.getenv("APP_ACTIVITY"),

        "timeout": float(os.getenv("TIMEOUT", "10")),

        # Настройки BrowserStack
        "bstack": {
            "user": os.getenv("BSTACK_USER"),
            "key": os.getenv("BSTACK_KEY"),
            "project": os.getenv("BSTACK_PROJECT"),
            "build": os.getenv("BSTACK_BUILD"),
            "session": os.getenv("BSTACK_SESSION"),
            "app": os.getenv("BSTACK_APP"),
        }
    }
