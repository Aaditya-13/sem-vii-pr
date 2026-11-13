import os
from bs4 import BeautifulSoup

#input
keyword = input("search keyword: ").lower()

found = False

for file in os.listdir("website"):
    with open("website/" + file) as f:
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text().lower()

        if keyword in text:
            print("Page:", file)
            print("Title:", soup.h1.text)
            print("Link:", "website/" + file)
            print("----------------")
            found = True

if not found:
    print("No results found!")
