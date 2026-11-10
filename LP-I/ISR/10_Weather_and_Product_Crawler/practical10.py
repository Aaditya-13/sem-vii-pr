import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
SHOP_URL = "https://books.toscrape.com/"


def show_weather(city):
    place = requests.get(GEOCODE_URL, params={"name": city, "count": 1}, timeout=10).json()
    if not place.get("results"):
        print("City not found")
        return
    place = place["results"][0]
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }
    current = requests.get(WEATHER_URL, params=params, timeout=10).json()["current"]
    descriptions = {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                    45: "Fog", 61: "Rain", 71: "Snow", 80: "Rain showers", 95: "Thunderstorm"}
    print("Weather in", place["name"], place.get("country", ""))
    print("Temperature:", current["temperature_2m"], "°C")
    print("Wind speed:", current["wind_speed_10m"], "km/h")
    print("Description:", descriptions.get(current["weather_code"], "Other conditions"))


def crawl_products():
    page = requests.get(SHOP_URL, timeout=10)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "html.parser")
    for product in soup.select("article.product_pod"):
        link = product.select_one("h3 a")
        name = link["title"]
        price = product.select_one(".price_color").get_text(strip=True)
        print(name, "|", price, "|", urljoin(SHOP_URL, link["href"]))


show_weather(input("Enter a city: "))
print("\nProducts on the first page:")
crawl_products()
