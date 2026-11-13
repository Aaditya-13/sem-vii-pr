
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# PART 1: WEATHER REPORT

city = input("Enter city name: ")

geo_url = "https://geocoding-api.open-meteo.com/v1/search"
data = requests.get(geo_url, params={"name": city, "count": 1}).json()

if "results" in data:
    place = data["results"][0]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }

    weather = requests.get(url, params=params).json()["current"]

    codes = {
        0: "Clear sky", 1: "Mainly clear",
        2: "Partly cloudy", 3: "Cloudy",
        45: "Foggy", 61: "Rain",
        63: "Moderate rain", 65: "Heavy rain",
        95: "Thunderstorm"
    }

    print("\n--- WEATHER REPORT ---")
    print("City:", place["name"])
    print("Temperature:", weather["temperature_2m"], "°C")
    print("Wind Speed:", weather["wind_speed_10m"], "km/h")
    print("Description:", codes.get(weather["weather_code"], "Other conditions"))
else:
    print("City not found!")


# PART 2: E-COMMERCE WEB CRAWLER

url = "https://books.toscrape.com/"
count = 0

print("\n--- PRODUCT DETAILS ---")

while url and count < 5:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("article", class_="product_pod")

    for p in products:
        if count == 5:
            break

        name = p.h3.a["title"]
        price = p.find("p", class_="price_color").text
        link = urljoin(url, p.h3.a["href"])

        print("\nProduct:", name)
        print("Price:", price)
        print("Link:", link)

        count += 1

    next_page = soup.select_one("li.next a")
    url = urljoin(url, next_page["href"]) if next_page and count < 5 else None

print("\nCrawling completed!")
