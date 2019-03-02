from Configuration.sources.loader import Loader
from threading import Thread
from time import sleep


class LoadersPool:
    actualize_period_seconds = 1

    def __init__(self):
        self._loaders_paths = dict()
        self._loaders = set()
        self._loaders_actualize_thread = Thread(target=self._actualize, daemon=True)
        self._loaders_actualize_thread.start()

    def get_or_add(self, receiver, path) -> Loader:
        loader = self._loaders_paths\
            .setdefault(path, {})\
            .setdefault(receiver, Loader(receiver, path))
        self._loaders.add(loader)
        return loader

    def _actualize(self):
        while True:
            sleep(LoadersPool.actualize_period_seconds)
            for loader in self._loaders:
                loader.load_config()
