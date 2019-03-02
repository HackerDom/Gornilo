from time import sleep
from Monitor.config import MonitorConfiguration

# just for testing hot properties

while True:
    config = MonitorConfiguration()
    print(config.api_key)
    print(config.indexer)
    print(MonitorConfiguration.api_key.fget(""))
    sleep(1)
