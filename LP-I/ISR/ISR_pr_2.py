
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import scoring
import os

# 1. Create Inverted Index
os.makedirs("myindex", exist_ok=True)

schema = Schema(id=ID(stored=True), content=TEXT(stored=True))
ix = create_in("myindex", schema)

# 2. Add Documents
writer = ix.writer()
writer.add_document(id="1", content="Python programming language Java")
writer.add_document(id="2", content="Java programming language")
writer.add_document(id="3", content="Python machine learning")
writer.commit()

print("Documents indexed successfully!")

# 3. Boolean Search
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("Java AND programming")
    results = searcher.search(query, limit=None)

    print("\n1. BOOLEAN SEARCH")
    print("Query: Python AND programming")

    for r in results:
        print("Document:", r["id"])
        print("Content:", r["content"])

# 4. Ranked Search using BM25F
with ix.searcher(weighting=scoring.BM25F()) as searcher:
    query = QueryParser("content", ix.schema).parse("Java OR learning")
    results = searcher.search(query, limit=None)

    print("\n2. RANKED SEARCH")

    for r in results:
        print("Document:", r["id"])
        print("Content:", r["content"])
        print("Score:", round(r.score, 2))

print("\nDocument Retrieval Completed Successfully!")
