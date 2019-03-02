from Configuration.sources.loaders_pool import LoadersPool
from Configuration.sources.base_source import Source
from Configuration.sources.json_source import JsonSource

from typing import Type

__loaders_pool = LoadersPool()

# todo find bug with multiple props + ctor provides non hot class (snapshot)


def __configuration(receiver: Type[Source], path: str):
    current_loader = __loaders_pool.get_or_add(receiver, path)

    def wrapper(cls: type):
        for annotation, obj in cls.__annotations__.items():
            try:
                hot_property = property(lambda _: obj(current_loader[annotation]))
            except KeyError:
                hot_property = property(lambda _: obj())
            setattr(cls, annotation, hot_property)
        return cls
    return wrapper


def json_source(path: str):
    return __configuration(JsonSource, path)


def github_source(path: str):
    pass
