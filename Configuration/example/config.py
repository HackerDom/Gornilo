from configuration import json_source


@json_source("config.json")
class MonitorConfiguration:
    api_key: str
    indexer: int = 4
