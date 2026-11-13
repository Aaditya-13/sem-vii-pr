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

# inverted_index = {} #for mapping

# for doc_id, text in documents:
#     for word in set(text.lower().split()):
#         inverted_index.setdefault(word, []).append(doc_id)

# for word, ids in sorted(inverted_index.items()):
#     print(word, "->", ids)


# Print Mapping
# with ix.searcher() as searcher:
#     reader = searcher.reader()

#     print("\nInverted Index:")
#     for word in sorted(reader.lexicon("content")):
#         postings = reader.postings("content", word)
#         document_ids = []

#         while postings.is_active():
#             number = postings.id()
#             document_ids.append(searcher.stored_fields(number)["id"])
#             postings.next()

#         print(word.decode("utf-8"), "->", document_ids)

# 3. Boolean Search
with ix.searcher() as searcher:
    boolean_input = input("\nEnter Boolean query (example: Java AND programming): ")
    query = QueryParser("content", ix.schema).parse(boolean_input)
    results = searcher.search(query, limit=None)

    print("\n1. BOOLEAN SEARCH")
    print("Query:", boolean_input)

    for r in results:
        print("Document:", r["id"])
        print("Content:", r["content"])

# 4. Ranked Search using BM25F
with ix.searcher(weighting=scoring.BM25F()) as searcher:
    ranked_input = input("\nEnter ranked search query (example: Java OR learning): ")
    query = QueryParser("content", ix.schema).parse(ranked_input)
    results = searcher.search(query, limit=None)

    print("\n2. RANKED SEARCH")
    print("Query:", ranked_input)

    for r in results:
        print("Document:", r["id"])
        print("Content:", r["content"])
        print("Score:", round(r.score, 2))

print("\nDocument Retrieval Completed Successfully!")
