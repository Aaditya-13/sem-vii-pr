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
