from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re

SITE = Path(__file__).parent / "website"


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.words = []

    def handle_data(self, text):
        self.words.extend(re.findall(r"[a-z]+", text.lower()))


pages = {}
for file in SITE.rglob("*.html"):
    parser = TextParser()
    parser.feed(file.read_text(encoding="utf-8"))
    pages[file] = Counter(parser.words)

index = {}
for file, words in pages.items():
    for word, count in words.items():
        index.setdefault(word, {})[file] = count

query = input("Search the website: ").lower()
scores = {}
for word in re.findall(r"[a-z]+", query):
    for file, count in index.get(word, {}).items():
        scores[file] = scores.get(file, 0) + count

print("Search results:")
for file, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(score, file.relative_to(SITE))
if not scores:
    print("No matching pages")
