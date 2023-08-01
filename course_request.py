from requests import get
from time import time


def getCurrentCourse():
    params = {
        "symbol": "EUR_RUB__TOD",
        "classcode": "CETS",
        "resolution": 60,
        "from": round(time() - 72 * 3600),
        "to": round(time())
    }
    response = get("https://api.bcs.ru/udfdatafeed/v1/history", params)
    data = response.json()
    if response:
        result = data.get("c")[-1] if data.get("c") else None
    else:
        result = None
    return result