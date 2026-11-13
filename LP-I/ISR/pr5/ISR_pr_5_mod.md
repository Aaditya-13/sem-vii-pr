# ISR Practical 5 Modified: Simpler Weather and Product Crawler

## Aim

Fetch current weather for a city and extract a few product details from an e-commerce practice site with a shorter crawler.

## How the code works

### Weather report

1. It asks for a city and sends that name to Open-Meteo's geocoding endpoint.
2. If a place is found, it sends its latitude and longitude to the forecast endpoint and requests current temperature, wind speed, and weather code.
3. A short `if/elif` block turns selected weather codes into descriptions: `0` is clear sky, `1`, `2`, and `3` are cloudy, and other codes become `Other conditions`.
4. It prints the city and the three requested weather values. If no city result is returned, it prints `City not found!`.

### Product crawler

1. It downloads and parses the first Books to Scrape page.
2. It selects the first five product cards and prints each title, price, and full product link.
3. `urljoin` combines the website URL with each product's relative link.

## Run

Install dependencies with `python -m pip install requests beautifulsoup4`, then run `python ISR_pr_5_mod.py`. Internet access is required.

## Difference from the original Practical 5 file


## Code with explanation

### City lookup

    city = input("Enter city name: ")
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_data = requests.get(
        geo_url, params={"name": city, "count": 1}
    ).json()

The first request searches for the city and asks for one location result. json() gives a Python dictionary.

    if geo_data.get("results"):
        place = geo_data["results"][0]

get checks that a non-empty result list exists. place is the first city match, including coordinates.

### Get weather and create a description

    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }
    weather = requests.get(weather_url, params=params).json()["current"]

The forecast request sends the coordinates and asks for the three current weather fields. weather stores the current part of the response.

    code = weather["weather_code"]
    if code == 0:
        description = "Clear sky"
    elif code in [1, 2, 3]:
        description = "Cloudy"
    else:
        description = "Other conditions"

code is numeric. The if/elif/else converts some values to descriptions. Every branch assigns description, so the later print can use it. Other codes get the fallback.

    print("City:", place["name"])
    print("Temperature:", weather["temperature_2m"], "Celsius")
    print("Wind Speed:", weather["wind_speed_10m"], "km/h")
    print("Description:", description)

These lines display the requested weather report. The outer else prints City not found if geocoding returns no match.

### Crawl the first page

    url = "https://books.toscrape.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

This downloads only the first product page and parses the HTML.

    for product in soup.select("article.product_pod")[:5]:
        name = product.select_one("h3 a")["title"]
        price = product.select_one(".price_color").get_text(strip=True)
        link = urljoin(url, product.select_one("h3 a")["href"])

select finds product cards and [:5] keeps the first five. The selectors read the product title and price. urljoin makes the relative href a complete link. The print calls display the product details.

### Main difference from original

This version avoids the page counter and pagination. It fetches the first page, prints five products, and uses a short if/elif weather description.

