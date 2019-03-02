from Configuration.sources.base_source import Source
from json import load


class JsonSource(Source):
    def get(self, path):
        with open(path) as file:
            return load(file)
