from datetime import datetime
from logging import getLogger
from typing import Type

from Configuration.sources.base_source import Source


logger = getLogger(__name__)


class Loader:
    idle_seconds = 5

    def __init__(self, source_factory: Type[Source], path: str):
        self._source_factory = source_factory
        self._path = path
        self._cached_config = {}
        self._load_time = datetime.utcnow()
        self._update_config()

    def __getitem__(self, item):
        return self._cached_config[item]

    def load_config(self) -> dict:
        try:
            if not self._cached_config:
                self._update_config()
                return self._cached_config

            if (datetime.utcnow() - self._load_time).seconds < Loader.idle_seconds:
                return self._cached_config

            self._update_config()
            return self._cached_config

        except Exception as e:
            logger.error(f"Configuration could not be loaded due to {e}, {e.__traceback__}")
            return self._cached_config

    def _update_config(self):
        try:
            self._cached_config = self._source_factory().get(self._path)
            self._load_time = datetime.utcnow()
        except Exception as e:
            logger.error(f"Configuration could not be updated due to {e}, {e.__traceback__}")
