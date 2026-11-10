from urllib.request import urlopen
import json


with urlopen("http://127.0.0.1:8000/") as response:
    data = json.loads(response.read().decode())

print("Service response:", data["message"])
