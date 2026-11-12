
import numpy as np
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Five sample documents
docs = [
    "Government announces economic policies",
    "Government supports economic growth",
    "Artificial intelligence changes technology",
    "Technology uses artificial intelligence",
    "Cricket players play matches"
]

# 2. Conflation using Porter Stemmer
stemmer = PorterStemmer()

docs = [
    " ".join(stemmer.stem(word) for word in doc.lower().split())
    for doc in docs
]

print("Conflated Documents:")
print(*docs, sep="\n")

# 3. TF-IDF Document Representation
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)

print("\nDocument Representation:")
print(X.toarray().round(2))

# 4. Single-Pass Clustering
clusters = []
threshold = 0.20

for i in range(len(docs)):

    scores = []

    for cluster in clusters:
        centroid = np.asarray(X[cluster].mean(axis=0)).ravel()
        similarity = cosine_similarity(X[i], centroid.reshape(1, -1))[0][0]
        scores.append(similarity)

    if scores and max(scores) >= threshold:
        best_cluster = scores.index(max(scores))
        clusters[best_cluster].append(i)

    else:
        clusters.append([i])

# 5. Display Final Clusters
print("\nFinal Clusters:")

for i, cluster in enumerate(clusters):
    print("Cluster", i + 1, ":",
          [document + 1 for document in cluster])

print("\nClustering Completed Successfully!")
