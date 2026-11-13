import requests

url = "http://127.0.0.1:5000/students"
response = requests.get(url)
response.raise_for_status()

for student in response.json():
    print(student["id"], student["name"], student["course"])
