import requests
import json

uri = "http://data.europa.eu/esco/occupation/c706886d-5bc7-4430-9a72-051fc483235f"
url = f"https://ec.europa.eu/esco/api/resource/occupation?uri={uri}&language=en"
resp = requests.get(url)
print(json.dumps(resp.json(), indent=2))
