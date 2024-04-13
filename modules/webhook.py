import requests, time
from modules.sysLogger import logger

def send(server,event_key):
    rCode = -1
    start = time.time()
    try:
        while rCode !=200 and time.time() < start + 1:
            webhook_url = f"{server}/api/webhook/{event_key}"
            response = requests.post(webhook_url)
            rCode = response.status_code
            time.sleep(0.5)
    except Exception as e:
        logger.warning(e)

    return rCode