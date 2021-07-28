from loguru import logger

from src.config import SystemConfig
from src.core.command import CommandService
from src.storage.cache.definition import Cache


class System:
    @staticmethod
    def on_start():
        logger.info("Triggering on_start events")
        SystemConfig.load()
        Cache.start()
        CommandService.load_defaults()

    @staticmethod
    def on_stop():
        logger.info("Triggering on_stop events")
        Cache.stop()
