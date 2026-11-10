# Practical 10 Weather API and Product Crawler

## Aim

Fetch current weather for a city and crawl a product listing page to extract product names, prices, and links.

## Theory

A weather API returns structured data such as JSON. The program first looks up a city's coordinates, then requests its current temperature, wind speed, and weather code. It turns common weather codes into short descriptions.

A web crawler requests a page, parses its HTML, finds product cards with CSS selectors, and collects details and links. This example uses Books to Scrape, a fictional bookstore sandbox made for scraping practice ([sandbox information](https://sites.toscrape.com/)). It reads only the first page.

## Run

Install the libraries:

```bash
python -m pip install requests beautifulsoup4
```

From this practical's folder run:

```bash
python practical10.py
```

Enter a city name when prompted. An internet connection is required for both requests. The weather example uses the Open-Meteo geocoding and forecast APIs; their documentation describes the city lookup and current weather fields ([Geocoding API](https://open-meteo.com/en/docs/geocoding-api), [Weather API](https://open-meteo.com/en/docs)).

For Jupyter, open `Practical_10.ipynb` with this folder as the working directory and run the cells in order. Change the `city` variable in the notebook to try another location.

## Code

```python
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
```

## Code explanation line by line

Line numbers refer to `practical10.py`.

| Line | Explanation |
|---:|---|
| 1-3 | Import HTTP requests, HTML parsing, and URL joining. |
| 5-7 | Set the geocoding, weather, and bookstore URLs. |
| 10-14 | Look up the city and stop if it was not found. |
| 15-22 | Get the city's coordinates and request its current weather. |
| 23-28 | Convert common weather codes to descriptions and print the report. |
| 31-34 | Request the bookstore page and parse its HTML. |
| 35-39 | Find each product card and print its title, price, and full link. |
| 42-44 | Ask for a city, show its weather, then crawl the first product page. |

## Viva questions with answers

1. **What is an API?** A way for one program to request data or services from another program.
2. **What is JSON?** A text format commonly used to send structured data over an API.
3. **Why does the program geocode a city first?** The forecast API needs latitude and longitude coordinates.
4. **What does `timeout=10` do?** It stops the request from waiting indefinitely if the server does not respond.
5. **What does a weather code represent?** A numeric label for a condition such as clear sky, rain, or snow.
6. **What is web crawling?** Automatically requesting web pages and collecting selected information from them.
7. **What does BeautifulSoup do?** It parses HTML so the program can find elements and text.
8. **What is a CSS selector?** A pattern for selecting HTML elements, such as `article.product_pod`.
9. **Why use `urljoin`?** It turns a product's relative link into a complete URL.
10. **What details does this crawler collect?** Product title, price, and link from the first listing page.
