# Practical 8 Retrieval Evaluation Metrics

## Aim

Rank documents for query q1 and calculate Precision, Recall, F-measure, E-measure, and NDCG from relevance judgments.

## Theory

Precision measures how many retrieved documents are relevant. Recall measures how many of all relevant documents were retrieved. F-measure combines precision and recall; here F1 is used. E-measure is calculated as `1 - F1`. NDCG rewards relevant documents that appear higher in the ranking and normalizes the score against an ideal ranking.

The program uses TF-IDF and cosine similarity to rank documents, then compares that ranking with the q1 relevance labels.

## Files and run

The program reads the following files from `data/`:

- `documents/*.txt`: one text document per file; the filename (without `.txt`) is its ID.
- `query.txt`: one line beginning with the query ID, such as `1 effect of airflow over an aerofoil`.
- `qrels.txt`: one relevance judgment per line in `query_id document_id grade` format.

The included five aerodynamics examples are a small demonstration set. For the real-world lab, download the Cranfield collection, which includes documents, queries, and relevance assessments, from the [University of Glasgow collection page](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/). Put q1's document texts in `data/documents/`, its query in `data/query.txt`, and q1 judgments in `data/qrels.txt`. The code reads one text file per document and the simple qrels format above.

Install the library and run from this practical's folder:

```bash
python -m pip install scikit-learn
python practical8.py
```

To run the notebook, open `Practical_8.ipynb` with this practical folder as the working directory and run its cells from top to bottom.

## Code

```python
from pathlib import Path
import math

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"
TOP_K = 3

documents = {file.stem: file.read_text(encoding="utf-8")
             for file in sorted((DATA / "documents").glob("*.txt"))}
query_line = (DATA / "query.txt").read_text(encoding="utf-8").strip()
query = query_line.split(maxsplit=1)[1]
qrels = {}
for line in (DATA / "qrels.txt").read_text(encoding="utf-8").splitlines():
    query_id, doc_id, grade = line.split()
    if query_id == "1":
        qrels[doc_id] = max(0, int(grade))

doc_ids = list(documents)
vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(documents.values())
query_vector = vectorizer.transform([query])
scores = cosine_similarity(query_vector, doc_vectors).ravel()
ranked = sorted(zip(doc_ids, scores), key=lambda item: item[1], reverse=True)
top_results = ranked[:TOP_K]

relevant_found = sum(qrels.get(doc_id, 0) > 0 for doc_id, score in top_results)
total_relevant = sum(grade > 0 for grade in qrels.values())
precision = relevant_found / TOP_K
recall = relevant_found / total_relevant
f_measure = 2 * precision * recall / (precision + recall) if precision + recall else 0
e_measure = 1 - f_measure

def dcg(grades):
    return sum((2**grade - 1) / math.log2(rank + 1)
               for rank, grade in enumerate(grades, start=1))

retrieved_grades = [qrels.get(doc_id, 0) for doc_id, score in top_results]
ideal_grades = sorted(qrels.values(), reverse=True)[:TOP_K]
ndcg = dcg(retrieved_grades) / dcg(ideal_grades) if dcg(ideal_grades) else 0

print("Top documents:")
for rank, (doc_id, score) in enumerate(top_results, start=1):
    print(rank, doc_id, round(score, 3), "relevance:", qrels.get(doc_id, 0))
print("\nPrecision@3:", round(precision, 3))
print("Recall@3:   ", round(recall, 3))
print("F-measure:  ", round(f_measure, 3))
print("E-measure:  ", round(e_measure, 3))
print("NDCG@3:     ", round(ndcg, 3))
```

## Code explanation line by line

Line numbers refer to `practical8.py`.

| Line | Explanation |
|---:|---|
| 1-5 | Import file paths, logarithms, TF-IDF, and cosine similarity. |
| 7-8 | Choose the data folder and evaluate the top three results. |
| 10-13 | Read document texts and extract the query text after its ID. |
| 14-18 | Read qrels and keep relevance judgments for q1; negative grades count as not relevant. |
| 20-26 | Vectorize the documents and query, calculate cosine scores, and rank documents. |
| 28-29 | Count relevant retrieved documents and all relevant q1 documents. |
| 30-33 | Calculate Precision@3, Recall@3, F1, and E-measure. |
| 35-37 | Calculate discounted cumulative gain from relevance grades. |
| 39-41 | Compare retrieved DCG with the ideal DCG to get NDCG@3. |
| 43-50 | Print the ranked results and the five evaluation measures. |

## A/B testing for search interfaces

A/B testing compares two interface versions. Randomly show some users version A (the current search page) and others version B (for example, a new ranking or filter layout). Give both groups similar search tasks. Compare task success, relevant results found, time to find an item, and user feedback. A higher click rate alone does not prove that search quality improved.

Example feedback themes to discuss in class:

- **Amazon-style product search:** “The size filter is selected, but I still see products in other sizes.”
- **Netflix-style recommendations:** “I keep seeing titles I have already watched.”

These are illustrative feedback examples, not direct user quotes. In a real A/B test, collect feedback from participants and pair it with search measures.

## Viva questions with answers

1. **What is precision?** The fraction of retrieved documents that are relevant.
2. **What is recall?** The fraction of all relevant documents that were retrieved.
3. **What is F-measure?** A combined score based on precision and recall; this practical uses F1.
4. **What is E-measure here?** The complement of F1, calculated as `1 - F1`.
5. **What is NDCG?** A measure that rewards relevant results near the top and compares them with an ideal ranking.
6. **What is a qrel?** A relevance judgment that says how relevant a document is to a query.
7. **Why use TF-IDF in this practical?** To turn documents and the query into vectors for similarity ranking.
8. **What does cosine similarity do?** It scores how similar the query vector is to each document vector.
9. **What is A/B testing?** A controlled comparison of two interface versions using different user groups.
10. **Why collect user feedback as well as scores?** Scores show retrieval performance, while feedback helps explain user experience problems.
