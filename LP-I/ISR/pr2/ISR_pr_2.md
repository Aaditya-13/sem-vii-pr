# ISR Practical 2: Inverted Index and Whoosh Search

## Aim

Index sample documents with Whoosh, then demonstrate Boolean search and ranked search.

## How the code works

1. **Imports:** Whoosh supplies the index, schema, query parser, and BM25F scoring. `os` creates the index folder.
2. **Create index:** `os.makedirs("myindex", exist_ok=True)` ensures a folder exists. `Schema` defines a stored document ID and searchable, stored content. `create_in` creates the Whoosh index in that folder.
3. **Add documents:** `writer.add_document(...)` adds three sample texts. `writer.commit()` saves the index. Whoosh builds its inverted index internally. The commented mapping examples are inactive and do not run.
4. **Boolean search:** The program asks for a query, parses it against the `content` field, and prints matching IDs and text. Use uppercase operators such as `AND` and `OR`, for example `Java AND programming`.
5. **Ranked search:** The program asks for a second query. BM25F scores and orders matching documents; the code prints the score with each result.

## Example

For `Java AND programming`, documents 1 and 2 match because both contain both terms. For `Java OR learning`, documents with either term can match and are shown with relevance scores.

## Run

Install Whoosh with `python -m pip install Whoosh`, then run `python ISR_pr_2.py`. The `myindex` path is relative to the folder from which you launch Python.

## Note


## Code with explanation

### Create the Whoosh index

    os.makedirs("myindex", exist_ok=True)
    schema = Schema(id=ID(stored=True), content=TEXT(stored=True))
    ix = create_in("myindex", schema)

os.makedirs creates the index folder if needed. The schema defines two fields: stored IDs and stored searchable text. create_in creates the Whoosh index in that folder. Whoosh creates the inverted index internally.

### Add documents and save

    writer = ix.writer()
    writer.add_document(id="1", content="Python programming language Java")
    writer.add_document(id="2", content="Java programming language")
    writer.add_document(id="3", content="Python machine learning")
    writer.commit()

writer opens the index for writing. Each add_document adds one sample. commit saves all three. The commented mapping code in the file starts with #, so it does not execute.

### Boolean search

    with ix.searcher() as searcher:
        boolean_input = input("Enter Boolean query: ")
        query = QueryParser("content", ix.schema).parse(boolean_input)
        results = searcher.search(query, limit=None)

The with block opens a searcher and closes it when finished. input lets a user type a query. QueryParser targets the content field; parse converts typed text into a Whoosh query. search runs it and limit=None asks for all matches. For Java AND programming, documents 1 and 2 match because both contain both words.

    for result in results:
        print("Document:", result["id"])
        print("Content:", result["content"])

Each result contains stored fields, so the loop prints its ID and original content.

### Ranked search with BM25F

    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        ranked_input = input("Enter ranked search query: ")
        query = QueryParser("content", ix.schema).parse(ranked_input)
        results = searcher.search(query, limit=None)

BM25F tells Whoosh how to score and order matching documents. This is a second search using a second typed query.

    for result in results:
        print("Document:", result["id"])
        print("Content:", result["content"])
        print("Score:", round(result.score, 2))

result.score is the relevance score calculated by Whoosh; round only controls how many decimals are shown. Use uppercase Boolean operators such as AND and OR.

