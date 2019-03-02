from Configuration.sources.loaders_pool import LoadersPool, Loader
from Configuration.sources.base_source import Source
from Configuration.sources.json_source import JsonSource

from typing import Type

__loaders_pool = LoadersPool()


def _patch_instance(instance_snapshot: Source, loader: Loader):
    for annotation, obj in instance_snapshot.__annotations__.items():
        try:
            setattr(instance_snapshot, annotation, obj(loader[annotation]))
        except KeyError:
            if not hasattr(instance_snapshot, annotation):
                setattr(instance_snapshot, annotation, obj())


def __configuration(receiver: Type[Source], path: str):
    current_loader = __loaders_pool.get_or_add(receiver, path)

    def wrapper(cls: type):
        cls.__init__ = lambda x: _patch_instance(x, current_loader)
        return cls

    return wrapper


def json_source(path: str):
    return __configuration(JsonSource, path)


def github_source(path: str):
    pass
