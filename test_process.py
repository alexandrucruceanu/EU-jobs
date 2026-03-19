import requests
import json
from bs4 import BeautifulSoup

uri = "http://data.europa.eu/esco/occupation/c706886d-5bc7-4430-9a72-051fc483235f"
url = f"https://ec.europa.eu/esco/api/resource/occupation?uri={uri}&language=en"
resp = requests.get(url)
data = resp.json()

print(f"Title: {data.get('title')}")
print(f"Code: {data.get('code')}")

desc = data.get("description", {}).get("en", {}).get("literalForm", "")
# Clean HTML tags using BeautifulSoup
soup = BeautifulSoup(desc, "html.parser")
print(f"Description: {soup.get_text().strip()}")

skills = data.get("_links", {}).get("hasEssentialSkill", [])
print("\nEssential Skills:")
for s in skills:
    print("- " + s.get("title", ""))

