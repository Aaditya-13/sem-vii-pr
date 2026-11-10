# Practical 7 Inverted Index and Whoosh Search

## Aim

Build an inverted index from text files and search them using Boolean and TF-IDF ranked retrieval with Whoosh.

## Theory

An **inverted index** maps each word to the IDs of documents containing it. A **Boolean search** uses operators such as `AND` to require terms. A **ranked search** orders matching documents by score. This program uses Whoosh's TF-IDF weighting for the ranked query; see the [Whoosh search guide](https://whoosh.readthedocs.io/en/latest/searching.html).

## Run

The program and notebook read `.txt` files from `data/`. Five sample files are included. Install Whoosh once:

```bash
python -m pip install Whoosh
```

Run the Python program from this practical's folder:

```bash
python practical7.py
```

Or open `Practical_7.ipynb` in Jupyter with this folder as the working directory and run its cells from top to bottom. Change the two query strings in the last steps to try other searches. To search your own documents, replace or add UTF-8 `.txt` files in `data/`.

## Code

```python
import re
from collections import defaultdict
from pathlib import Path

from whoosh import scoring
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in
from whoosh.qparser import OrGroup, QueryParser

DATA = Path(__file__).parent / "data"
INDEX = Path(__file__).parent / "whoosh_index"
documents = [(file.stem, file.read_text(encoding="utf-8"))
             for file in sorted(DATA.glob("*.txt"))]

# 1. Build a word -> document IDs inverted index.
inverted_index = defaultdict(list)
for doc_id, text in documents:
    for word in set(re.findall(r"\w+", text.lower())):
        inverted_index[word].append(doc_id)

for word in sorted(inverted_index):
    print(word, "->", inverted_index[word])

# 2. Build a Whoosh index from the same documents.
INDEX.mkdir(exist_ok=True)
schema = Schema(doc_id=ID(stored=True), content=TEXT(stored=True))
index = create_in(str(INDEX), schema)
with index.writer() as writer:
    for doc_id, text in documents:
        writer.add_document(doc_id=doc_id, content=text)

# 3. Boolean search: both terms must appear.
with index.searcher() as searcher:
    parser = QueryParser("content", schema=index.schema)
    results = searcher.search(parser.parse("machine AND learning"))
    for result in results:
        print("Boolean:", result["doc_id"], result["content"])

# 4. Ranked search: match either term and rank with TF-IDF.
with index.searcher(weighting=scoring.TF_IDF()) as searcher:
    parser = QueryParser("content", schema=index.schema, group=OrGroup)
    results = searcher.search(parser.parse("python data"))
    for result in results:
        print("Ranked:", result["doc_id"], round(result.score, 2), result["content"])
```

## Code explanation line by line

Line numbers refer to `practical7.py`.

| Line | Explanation |
|---:|---|
| 1-3 | Import word matching, the postings-list dictionary, and file paths. |
| 5-8 | Import Whoosh's index, fields, query parser, and scoring tools. |
| 10-13 | Point to `data/` and read each text file with its filename as its ID. |
| 16-19 | For every document, add its ID to the postings list for each unique word. |
| 21-22 | Print the manual inverted index. |
| 25-27 | Make the index folder, define its fields, and create the Whoosh index. |
| 28-30 | Add the documents to Whoosh. The writer saves the index when the block ends. |
| 33-37 | Search for documents containing both `machine` and `learning`. |
| 40-44 | Search for either `python` or `data`, rank matches with TF-IDF, and print scores. |

## Viva questions with answers

1. **What is an inverted index?** A structure that maps each word to the documents containing it.
2. **What is a postings list?** The document ID list stored for a word.
3. **Why use an inverted index?** It lets a search engine find matching documents without scanning every document for every query.
4. **What does Boolean `AND` mean?** All query terms joined by `AND` must appear in a matching document.
5. **What is ranked retrieval?** Returning matching documents ordered by a relevance score.
6. **What does TF-IDF stand for?** Term Frequency–Inverse Document Frequency.
7. **Why use TF-IDF?** It gives more weight to terms frequent in a document but uncommon across the collection.
8. **What is a Whoosh schema?** The definition of document fields to store and search.
9. **What does `QueryParser` do?** It converts a query string into a query Whoosh can search.
10. **How do the two searches differ here?** Boolean search requires both terms; ranked search can match either term and orders matches by TF-IDF score.
