import os, math, random

# 1. Create documents
os.makedirs("documents", exist_ok=True)

docs = {
    "D1.txt": "Python programming and coding",
    "D2.txt": "Python machine learning",
    "D3.txt": "Java programming language",
    "D4.txt": "Python data science",
    "D5.txt": "Web development using HTML"
}

for name, text in docs.items():
    with open("documents/" + name, "w") as f:
        f.write(text)

# 2. Search documents
query = "Python programming"
relevant = ["D1.txt", "D2.txt", "D4.txt"]

results = []
for name in docs:
    text = open("documents/" + name).read().lower().split()
    if any(w in text for w in query.lower().split()):
        results.append(name)

# 3. Calculate evaluation metrics
TP = len(set(results) & set(relevant))
P = TP / len(results) if results else 0
R = TP / len(relevant) if relevant else 0
F = 2 * P * R / (P + R) if P + R else 0
E = 1 - F

scores = [1 if d in relevant else 0 for d in results]
dcg = sum(s / math.log2(i + 2) for i, s in enumerate(scores))
idcg = sum(s / math.log2(i + 2) for i, s in enumerate(sorted(scores, reverse=True)))
ndcg = dcg / idcg if idcg else 0

print("Retrieved:", results)
print("Relevant:", relevant)
print("Precision:", round(P, 2))
print("Recall:", round(R, 2))
print("F-measure:", round(F, 2))
print("E-measure:", round(E, 2))
print("NDCG:", round(ndcg, 2))

# 4. A/B Testing Simulation
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

# 5. Overview and feedback
print("""
A/B Testing: Compare original (A) and modified (B) interfaces
using CTR, search time and user satisfaction.

Amazon: Search filters and product relevance.
Netflix: Thumbnails and personalized recommendations.
""")
