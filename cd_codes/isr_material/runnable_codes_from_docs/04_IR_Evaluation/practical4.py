from pathlib import Path
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).parent
DOCUMENT_FOLDER = BASE / "cranfield"
QUERY_FILE = BASE / "TEST" / "query.txt"
RES_FOLDER = BASE / "TEST" / "RES"
TOP_K = 10

# Read Cranfield text files; each filename (for example 184.txt) is its document ID.
documents = {p.stem: p.read_text(encoding="utf-8", errors="ignore")
             for p in sorted(DOCUMENT_FOLDER.glob("*.txt"))}
print("Documents loaded:", len(documents))

# Each query line starts with its ID followed by query text.
queries = {}
for line in QUERY_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
    parts = line.split(maxsplit=1)
    if len(parts) == 2:
        queries[parts[0]] = parts[1]
print("Queries loaded:", len(queries))

# Relevance files use: query_id document_id relevance_grade.
q1_relevance = {}
for path in RES_FOLDER.glob("*"):
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[0] == "1":
                try:
                    q1_relevance[parts[1]] = float(parts[2])
                except ValueError:
                    pass

query = queries["1"]
document_ids = list(documents)
vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(documents.values())
query_vector = vectorizer.transform([query])
scores = cosine_similarity(query_vector, doc_vectors).ravel()
ranked = sorted(zip(document_ids, scores), key=lambda item: item[1], reverse=True)
top_results = ranked[:TOP_K]

relevant_retrieved = sum(q1_relevance.get(doc_id, 0) > 0 for doc_id, _ in top_results)
total_relevant = sum(grade > 0 for grade in q1_relevance.values())
precision = relevant_retrieved / TOP_K
recall = relevant_retrieved / total_relevant if total_relevant else 0
f_measure = 2 * precision * recall / (precision + recall) if precision + recall else 0
e_measure = 1 - f_measure

def dcg(grades):
    return sum(grade / math.log2(rank + 1)
               for rank, grade in enumerate(grades, start=1))

retrieved_grades = [max(0, q1_relevance.get(doc_id, 0))
                    for doc_id, _ in top_results]
ideal_grades = sorted(retrieved_grades, reverse=True)
dcg_value = dcg(retrieved_grades)
idcg = dcg(ideal_grades)
ndcg = dcg_value / idcg if idcg else 0

print("\nQUERY q1:", query)
print("\nTOP RESULTS")
for rank, (doc_id, score) in enumerate(top_results, start=1):
    print(rank, doc_id, round(score, 4), "relevance:", q1_relevance.get(doc_id, 0))
print("\nPrecision@10:", round(precision, 4))
print("Recall@10:   ", round(recall, 4))
print("F-measure:   ", round(f_measure, 4))
print("E-measure:   ", round(e_measure, 4))
print("DCG@10:      ", round(dcg_value, 4))
print("IDCG@10:     ", round(idcg, 4))
print("NDCG@10:     ", round(ndcg, 4))
print("Retrieved relevance:", retrieved_grades)
print("Ideal relevance:    ", ideal_grades)
