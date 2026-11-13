import math, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# 1. DOCUMENT COLLECTION (Embedded sample dataset)
# ============================================================

documents = {
    "D1": "Experimental investigation of heat transfer in aircraft engines",
    "D2": "Study of fluid mechanics and aerodynamic performance of wings",
    "D3": "Experimental analysis of heat transfer using cooling systems",
    "D4": "Aircraft design and aerodynamic characteristics",
    "D5": "Investigation of thermal energy and heat exchange",
    "D6": "Numerical study of fluid flow around an aircraft wing",
    "D7": "Computer programming using Python and Java",
    "D8": "Methods for measuring heat transfer in engineering systems",
    "D9": "A study of combustion in gas turbine engines",
    "D10": "Aerodynamics and performance of high speed aircraft",
    "D11": "Machine learning applications in data science",
    "D12": "Experimental study of cooling and thermal systems"
}

# ============================================================
# 2. QUERY AND RELEVANCE JUDGMENTS
# ============================================================

query_id = "q1"
query = "experimental investigation of heat transfer"

# 1 = relevant, 0 = not relevant
relevance = {
    "D1": 1,
    "D3": 1,
    "D5": 1,
    "D8": 1,
    "D12": 1,
    "D2": 0,
    "D4": 0,
    "D6": 0,
    "D7": 0,
    "D9": 0,
    "D10": 0,
    "D11": 0
}

print("QUERY:", query_id)
print("Query text:", query)

# ============================================================
# 3. TF-IDF VECTORIZATION
# ============================================================

document_ids = list(documents.keys())
document_texts = [documents[doc_id] for doc_id in document_ids]

vectorizer = TfidfVectorizer(stop_words="english")
document_vectors = vectorizer.fit_transform(document_texts)

query_vector = vectorizer.transform([query])

# ============================================================
# 4. COSINE SIMILARITY
# ============================================================

similarities = cosine_similarity(
    query_vector, document_vectors
).flatten()

# ============================================================
# 5. RANK DOCUMENTS
# ============================================================

ranked_indices = similarities.argsort()[::-1]

ranked_documents = [
    (document_ids[i], similarities[i])
    for i in ranked_indices
]

TOP_K = 10
top_results = ranked_documents[:TOP_K]

print("\nTOP 10 RETRIEVED DOCUMENTS")
print("-" * 55)
print(f"{'Rank':<8}{'Document':<12}{'Similarity':<15}{'Relevance'}")

for rank, (doc_id, score) in enumerate(top_results, start=1):
    rel = relevance[doc_id]
    print(f"{rank:<8}{doc_id:<12}{score:<15.4f}{rel}")

# ============================================================
# 6. PRECISION
# ============================================================

relevant_retrieved = sum(
    1 for doc_id, score in top_results
    if relevance[doc_id] > 0
)

precision = relevant_retrieved / len(top_results) if top_results else 0

# ============================================================
# 7. RECALL
# ============================================================

total_relevant = sum(
    1 for rel in relevance.values() if rel > 0
)

recall = relevant_retrieved / total_relevant if total_relevant else 0

# ============================================================
# 8. F-MEASURE
# ============================================================

if precision + recall == 0:
    f_measure = 0
else:
    f_measure = 2 * precision * recall / (precision + recall)

# ============================================================
# 9. E-MEASURE
# ============================================================

e_measure = 1 - f_measure

# ============================================================
# 10. DCG
# ============================================================

def dcg(relevance_scores):
    total = 0
    for position, rel in enumerate(relevance_scores, start=1):
        total += rel / math.log2(position + 1)
    return total

retrieved_relevance = [
    relevance[doc_id] for doc_id, score in top_results
]

DCG = dcg(retrieved_relevance)

# ============================================================
# 11. IDCG
# ============================================================

# Ideal ranking is based on all relevance judgments,
# limited to the same number of documents as the retrieved list.
ideal_relevance = sorted(relevance.values(), reverse=True)[:len(top_results)]

IDCG = dcg(ideal_relevance)

# ============================================================
# 12. NDCG
# ============================================================

NDCG = DCG / IDCG if IDCG > 0 else 0

# ============================================================
# 13. FINAL RESULTS
# ============================================================

print("\n" + "=" * 45)
print("FINAL EVALUATION RESULTS FOR", query_id)
print("=" * 45)

print("Precision@10 :", round(precision, 4))
print("Recall@10    :", round(recall, 4))
print("F-measure    :", round(f_measure, 4))
print("E-measure    :", round(e_measure, 4))
print("DCG@10       :", round(DCG, 4))
print("IDCG@10      :", round(IDCG, 4))
print("NDCG@10      :", round(NDCG, 4))

print("\nNDCG CALCULATION")
print("Retrieved relevance:", retrieved_relevance)
print("Ideal relevance    :", ideal_relevance)
print("NDCG = DCG / IDCG")


# ============================================================
# 14. A/B Testing
# ============================================================

random.seed(1)
n = 2000

cA = sum(random.random() < 0.10 for _ in range(n))
cB = sum(random.random() < 0.12 for _ in range(n))

pA, pB = cA/n, cB/n
pool = (cA + cB) / (2*n)
z = (pB-pA) / math.sqrt(pool*(1-pool)*(2/n))
pval = math.erfc(abs(z)/math.sqrt(2))

print("\nA/B TESTING")
print("CTR A:", round(pA, 3), "CTR B:", round(pB, 3))
print("Z-score:", round(z, 2), "P-value:", round(pval, 4))
print("Version B is better!" if pval < 0.05 and pB > pA else "No significant improvement")