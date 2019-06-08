from json import loads
from urllib.request import urlopen
from sources.base_source import Source


class ExternalJsonSource(Source):
    def get(self, path) -> dict:
        external_data = urlopen(path, timeout=5)\
                .read()\
                .decode()
        return loads(external_data)
