import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# PART 1: WEATHER REPORT
city = input("Enter city name: ")

geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_data = requests.get(geo_url, params={"name": city, "count": 1}).json()

if geo_data.get("results"):
    place = geo_data["results"][0]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }
    weather = requests.get(weather_url, params=params).json()["current"]

    code = weather["weather_code"]
    if code == 0:
        description = "Clear sky"
    elif code in [1, 2, 3]:
        description = "Cloudy"
    else:
        description = "Other conditions"

    print("\n--- WEATHER REPORT ---")
    print("City:", place["name"])
    print("Temperature:", weather["temperature_2m"], "Celsius")
    print("Wind Speed:", weather["wind_speed_10m"], "km/h")
    print("Description:", description)
else:
    print("City not found!")

# PART 2: PRODUCT CRAWLER (first page, first five products)
url = "https://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

print("\n--- PRODUCT DETAILS ---")
for product in soup.select("article.product_pod")[:5]:
    name = product.select_one("h3 a")["title"]
    price = product.select_one(".price_color").get_text(strip=True)
    link = urljoin(url, product.select_one("h3 a")["href"])

    print("\nProduct:", name)
    print("Price:", price)
    print("Link:", link)

print("\nCrawling completed!")
