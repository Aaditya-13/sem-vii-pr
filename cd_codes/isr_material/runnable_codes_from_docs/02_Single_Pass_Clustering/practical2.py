import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Folder containing the input text files
folder = Path(__file__).parent / "data"
documents = []
filenames = []

# Read all .txt files from the folder
for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        filenames.append(filename)
        with open(folder / filename, "r", encoding="utf-8") as file:
            documents.append(file.read())

# Convert documents into TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words="english")
tfidf = vectorizer.fit_transform(documents)

# Single-pass clustering
threshold = 0.10
clusters = []
leaders = []

for i in range(len(documents)):
    if len(leaders) == 0:
        clusters.append([i])
        leaders.append(i)
        continue

    similarities = []
    for leader in leaders:
        similarity = cosine_similarity(tfidf[i], tfidf[leader])[0][0]
        similarities.append(similarity)

    max_similarity = max(similarities)
    if max_similarity >= threshold:
        cluster_index = similarities.index(max_similarity)
        clusters[cluster_index].append(i)
    else:
        leaders.append(i)
        clusters.append([i])

# Display clusters
print("\nClusters Formed\n")
for i, cluster in enumerate(clusters):
    print("Cluster", i + 1)
    for document_index in cluster:
        print("   ", filenames[document_index])
    print()
