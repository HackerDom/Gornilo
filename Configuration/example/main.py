from time import sleep
from Configuration.example.config import MonitorConfiguration


saved_instance = MonitorConfiguration()

while True:
    dynamic_instance = MonitorConfiguration()
    print(f"""
        Saved key = {saved_instance.api_key}
        Dynamic key = {dynamic_instance.api_key}
        
        Saved index = {saved_instance.indexer}
        Dynamic key = {dynamic_instance.indexer}
    """)
    sleep(1)
