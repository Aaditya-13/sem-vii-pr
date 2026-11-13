
import os
from bs4 import BeautifulSoup

# Create website folder
os.makedirs("website", exist_ok=True)

# Create HTML pages
pages = {
    "python.html": "<h1>Python</h1><p>Python is a programming language.</p>",
    "java.html": "<h1>Java</h1><p>Java is used for application development.</p>",
    "ai.html": "<h1>Artificial Intelligence</h1><p>AI uses machine learning.</p>"
}

for name, content in pages.items():
    with open("website/" + name, "w") as f:
        f.write(content)

# Search engine
keyword = input("Enter search keyword: ").lower()

print("\nSearch Results:")
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
