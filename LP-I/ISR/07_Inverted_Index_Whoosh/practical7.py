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
