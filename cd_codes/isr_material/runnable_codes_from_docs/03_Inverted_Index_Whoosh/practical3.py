import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser, MultifieldParser

# Sample documents from the assignment
documents = [
    {"id": "1", "content": "Machine learning is a subset of artificial intelligence."},
    {"id": "2", "content": "Deep learning uses neural networks."},
    {"id": "3", "content": "Python is widely used in data science."},
    {"id": "4", "content": "Artificial intelligence includes machine learning and deep learning."},
    {"id": "5", "content": "Data science uses Python and machine learning."}
]

# Part 1: Build an inverted index
print("=" * 60)
print("PART 1 : BUILDING INVERTED INDEX")
print("=" * 60)
inverted_index = defaultdict(list)
for doc in documents:
    words = re.findall(r"\w+", doc["content"].lower())
    for word in set(words):
        inverted_index[word].append(doc["id"])

print("\nInverted Index\n")
for word in sorted(inverted_index):
    print(f"{word:15} -> {inverted_index[word]}")

# Part 2: Search using the inverted index
print("\n" + "=" * 60)
print("PART 2 : SEARCH USING INVERTED INDEX")
print("=" * 60)
query = input("\nEnter Search Word: ").lower().strip()
if query in inverted_index:
    print("\nDocuments Found\n")
    for doc_id in inverted_index[query]:
        for doc in documents:
            if doc["id"] == doc_id:
                print("Document", doc["id"])
                print(doc["content"], "\n")
else:
    print("\nNo Document Found")

# Part 3: Create the Whoosh index
print("\n" + "=" * 60)
print("PART 3 : WHOOSH INDEXING")
print("=" * 60)
index_dir = Path(__file__).parent / "whoosh_index"
if index_dir.exists():
    shutil.rmtree(index_dir)
index_dir.mkdir()
schema = Schema(id=ID(stored=True), content=TEXT(stored=True))
ix = create_in(str(index_dir), schema)
writer = ix.writer()
for doc in documents:
    writer.add_document(id=doc["id"], content=doc["content"])
writer.commit()
print("Whoosh Index Created Successfully")

# Part 4: Boolean search
print("\n" + "=" * 60)
print("PART 4 : BOOLEAN SEARCH")
print("=" * 60)
with ix.searcher() as searcher:
    parser = QueryParser("content", schema=ix.schema)
    boolean_input = input("\nEnter Boolean Query (Example: machine AND learning): ")
    results = searcher.search(parser.parse(boolean_input))
    if len(results) == 0:
        print("\nNo Match Found")
    else:
        print("\nBoolean Search Results\n")
        for result in results:
            print("Document:", result["id"])
            print(result["content"], "\n")

# Part 5: Vector-space search
print("\n" + "=" * 60)
print("PART 5 : VECTOR SPACE SEARCH")
print("=" * 60)
with ix.searcher() as searcher:
    parser = MultifieldParser(["content"], schema=ix.schema)
    vector_input = input("\nEnter Vector Search Query: ")
    results = searcher.search(parser.parse(vector_input))
    if len(results) == 0:
        print("\nNo Match Found")
    else:
        print("\nRanked Results\n")
        for result in results:
            print(f"Document : {result['id']}")
            print(f"Score    : {result.score:.2f}")
            print(result["content"])
            print("-" * 50)

print("\n" + "=" * 60)
print("PROGRAM COMPLETED SUCCESSFULLY")
print("=" * 60)
