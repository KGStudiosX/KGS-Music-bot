import json
import requests
from typing import Optional

def antihack(message: str) -> bool:
    for i in message:
        if i in ["$", "{", "("]:
            return False
    return True

def parsejson(radioid: Optional[int]=None):
    radioid, recordlist = radioid or 15016, json.loads(requests.get("https://www.radiorecord.ru/api/stations/now/").content)
    for i in recordlist["result"]:
        if i["id"] == radioid:
            return i["track"]
