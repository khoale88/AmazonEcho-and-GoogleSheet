import requests
import json

host = "http://35.164.41.209:8082"


def getMenu(section):
    endpoint = "/menu/"+section.lower()
    r = requests.get(url = host+endpoint)
    if r.status_code == 200:
        s = json.loads(r.content)
        return [item for sublist in s for item in sublist]

