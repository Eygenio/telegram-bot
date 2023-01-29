import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    """
    Класс Настройки сайта. Родитель: BaseSettings
     SecretStr: сайт API
     StrictStr: хост API
    """
    api_key: SecretStr = os.getenv("SITE_API", None)
    host_api: StrictStr = os.getenv("HOST_API", None)


class BotSettings(BaseSettings):
    """
    Класс Настройки бота. Родитель: BaseSettings
     SecretStr: сайт API
     StrictStr: хост API
    """
    bot_token: SecretStr = os.getenv("BOT_TOKEN", None)


DEFAULT_COMMANDS = (
    ('help', "Вывести справку"),
    ('history', "Вывести последние 10 команд"),
    ('low', "Вывести список самых старых автомобилей"),
    ('high', "Вывести список самых новых автомобилей")
)