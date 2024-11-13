import time
from zapv2 import ZAPv2

# Config
zap_api_key = 'YOUR_API_KEY'  # Replace with your ZAP API Key
zap_base_url = 'http://127.0.0.1:8080'  # ZAP base URL
context_name = 'VAMPI'  # Context name in ZAP
swagger_file_path = '/path/to/swagger.json'  # Full path to Swagger file

zap = ZAPv2(apikey=zap_api_key, proxies={'http': zap_base_url, 'https': zap_base_url})

def get_context_id(context_name):
    for context in zap.context.context_list:
        if context == context_name:
            return zap.context.context(context)['id']
    raise ValueError(f"Context '{context_name}' not found in ZAP.")

try:
    context_id = get_context_id(context_name)
    print(f"Importing Swagger from {swagger_file_path}...")
    zap.openapi.import_file(swagger_file_path, zap_base_url)

    print("Starting Spider...")
    spider_id = zap.spider.scan_as_user(context_id, 1, zap_base_url)
    time.sleep(5)
    while int(zap.spider.status(spider_id)) < 100:
        print(f"Spider progress: {zap.spider.status(spider_id)}%")
        time.sleep(2)
    print("Spider complete.")

    print("Starting AJAX Spider...")
    zap.ajaxSpider.scan(zap_base_url)
    time.sleep(5)
    while zap.ajaxSpider.status == 'running':
        print("AJAX Spider in progress...")
        time.sleep(2)
    print("AJAX Spider complete.")

    print("Starting Active Scan...")
    scan_id = zap.ascan.scan_as_user(context_id, 1, zap_base_url, recurse=True)
    time.sleep(5)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"Active Scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(2)
    print("Active Scan complete.")
    print("All requests have been logged in ZAP. Review results in the ZAP interface.")

except Exception as e:
    print(f"Error: {e}")
