import re
from collections import Counter
from pathlib import Path

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"
THRESHOLD = 0.20
stemmer = PorterStemmer()


def conflate(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return [stemmer.stem(word) for word in words if word not in ENGLISH_STOP_WORDS]


files = sorted(DATA.glob("*.txt"))
names = [file.name for file in files]
documents = [conflate(file.read_text(encoding="utf-8")) for file in files]

for name, words in zip(names, documents):
    print(name, dict(Counter(words)))

vectorizer = TfidfVectorizer(tokenizer=str.split, token_pattern=None, lowercase=False)
tfidf = vectorizer.fit_transform([" ".join(words) for words in documents])

clusters, leaders = [], []
for i in range(len(documents)):
    if not leaders:
        leaders.append(i)
        clusters.append([i])
        continue

    similarities = cosine_similarity(tfidf[i], tfidf[leaders]).ravel()
    best = similarities.argmax()
    if similarities[best] >= THRESHOLD:
        clusters[best].append(i)
    else:
        leaders.append(i)
        clusters.append([i])

for number, cluster in enumerate(clusters, start=1):
    print(f"\nCluster {number} (leader: {names[leaders[number - 1]]})")
    for i in cluster:
        print(" -", names[i])
