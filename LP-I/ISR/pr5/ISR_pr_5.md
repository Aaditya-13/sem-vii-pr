# ISR Practical 5: Weather API and Product Crawler

## Aim

Fetch current weather for a city and crawl product details and links from an e-commerce practice website.

## How the code works

### Weather report

1. The program asks for a city name.
2. The geocoding request sends the name to Open-Meteo and gets a matching place with latitude and longitude.
3. The forecast request sends those coordinates and asks for current temperature, wind speed, and weather code.
4. The `codes` dictionary converts some numeric weather codes into descriptions. Unknown codes display `Other conditions`.
5. The report prints the city, temperature, wind speed, and description.

There are two Open-Meteo requests because the geocoding endpoint finds coordinates and the forecast endpoint needs coordinates to return weather.

### Product crawler

1. The crawler requests the Books to Scrape home page and parses its HTML with BeautifulSoup.
2. It finds product cards, then extracts each title, price, and product link.
3. `urljoin` turns each relative product link into a full URL.
4. The loop stops after five products, following pagination only if it needs another page to reach five.

## Run

Install dependencies with `python -m pip install requests beautifulsoup4`, then run `python ISR_pr_5.py`. Internet access is required for both sections.

## Notes


## Code with explanation

### Imports

    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

requests downloads API responses and web pages. BeautifulSoup parses HTML. urljoin converts relative product links to full URLs.

### Geocode the city

    city = input("Enter city name: ")
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    data = requests.get(
        geo_url, params={"name": city, "count": 1}
    ).json()

The first request sends the city name to Open-Meteo's geocoding endpoint. params asks for one result. json() converts the response to a Python dictionary.

    if "results" in data:
        place = data["results"][0]

If results is present, place is its first location, including latitude and longitude.

### Fetch weather

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }
    weather = requests.get(url, params=params).json()["current"]

The forecast endpoint requires coordinates. current requests temperature, wind speed, and weather code. The second request gets the values for that location.

    codes = {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
             3: "Cloudy", 45: "Foggy", 61: "Rain",
             63: "Moderate rain", 65: "Heavy rain", 95: "Thunderstorm"}
    print("Description:",
          codes.get(weather["weather_code"], "Other conditions"))

The dictionary converts selected numeric weather codes into words. get returns the fallback for an unlisted code. The other print statements show city, temperature, and wind. The source has an encoding issue in the temperature unit text.

### Crawl products and follow pages

    url = "https://books.toscrape.com/"
    count = 0
    while url and count < 5:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("article", class_="product_pod")

url starts at the shop. count limits output to five. The loop downloads pages until five products are collected or there is no next URL. BeautifulSoup parses HTML and find_all locates product cards.

    for p in products:
        if count == 5:
            break
        name = p.h3.a["title"]
        price = p.find("p", class_="price_color").text
        link = urljoin(url, p.h3.a["href"])
        count += 1

The inner loop processes each card until the limit. It extracts the name, price, and relative href. urljoin creates an absolute link. count increments for each product.

    next_page = soup.select_one("li.next a")
    url = urljoin(url, next_page["href"]) if next_page and count < 5 else None

The code looks for a next-page link and follows it only if more products are needed. Otherwise it ends the while loop.

