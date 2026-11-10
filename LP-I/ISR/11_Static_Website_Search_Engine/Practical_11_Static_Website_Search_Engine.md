# Practical 11 Simple Search Engine for a Static Website

## Aim

Build a small search engine that reads static HTML pages, indexes their words, and returns pages matching a user's query.

## Theory

A search engine first reads pages and builds an **inverted index**: each word points to the pages where it appears. For a query, the program looks up each word, adds its term counts to a page score, and shows the highest-scoring pages first.

This practical searches a local static website. It does not need a web server or an internet connection. Python's built-in `HTMLParser` extracts page text, and the built-in `Counter` counts words.

## Files and run

- `website/` contains four static HTML pages to search.
- `practical11.py` builds the inverted index and searches it.
- `Practical_11.ipynb` performs the same steps in Jupyter.

No extra Python packages are needed. Open a terminal in this practical's folder and run:

```bash
python practical11.py
```

Enter a query such as `machine learning` or `python functions`. The program prints matching page names and their scores. Edit or add `.html` files in `website/` to change the searchable site.

For Jupyter, open `Practical_11.ipynb` with this practical folder as the working directory and run the cells from top to bottom.

## Code

```python
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
```

## Code explanation line by line

Line numbers refer to `practical11.py`.

| Line | Explanation |
|---:|---|
| 1-4 | Import word counting, HTML parsing, paths, and regular expressions. |
| 6 | Set the folder containing the static website. |
| 9-15 | Create a parser that collects lowercase words from HTML text. |
| 18-22 | Read every HTML page and count the words in it. |
| 24-27 | Build the inverted index: each word points to pages and its count in each page. |
| 29-33 | Read the query and add matching word counts to each page's score. |
| 35-37 | Print pages from highest score to lowest. |
| 38-39 | Show a message when no page contains any query word. |

## Viva questions with answers

1. **What is a static website?** A set of files, such as HTML pages, that are served as written rather than generated for each request.
2. **What does this search engine search?** The text inside local HTML files in the `website/` folder.
3. **What is an inverted index?** A mapping from each word to the pages that contain it.
4. **What is a term frequency?** The number of times a word appears in one page.
5. **How are the search results ranked?** The program adds the counts of query words in each page and sorts by that score.
6. **What does `HTMLParser` do?** It reads HTML structure and passes the text between tags to the program.
7. **Why convert words to lowercase?** So that `Python` and `python` match the same index entry.
8. **What is a crawler in this practical?** The part that visits each local HTML file and extracts its text for indexing.
9. **What happens if a query word is absent from the index?** It contributes no score to any page.
10. **How can the search engine cover more pages?** Add more HTML files under `website/`; the program finds them recursively.
