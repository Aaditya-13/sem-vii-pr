# Practical 6 Conflation and Single Pass Clustering

## Aim

Normalize words, represent documents with term frequencies, and group four or five text files using single-pass clustering.

## Theory

**Conflation** reduces related word forms to a common stem. This program lowercases words, removes English stop words, and applies the Porter stemmer. It counts the remaining terms to show each document's representation.

For clustering, TF-IDF turns the processed documents into vectors, and cosine similarity compares them. Single-pass clustering reads documents in order: a document joins the most similar existing cluster if its score meets the threshold; otherwise, it becomes the leader of a new cluster. Changing the order or threshold can change the result.

## Files

- `practical6.py` reads every `.txt` file in `data/`, prints term counts, and forms clusters.
- `Practical_6.ipynb` is a Jupyter version that reads the same `.txt` files from `data/`.
- `data/` contains five small practice news snippets. They are examples, not records from an actual news corpus.

## Run the Python program

Install Python 3, then install the two libraries:

```bash
python -m pip install nltk scikit-learn
```

From this folder run:

```bash
python practical6.py
```

No NLTK corpus download is needed. To try your own data, put four or five UTF-8 `.txt` files in `data/` and run again.

## Real-world data activity

Use four or five article bodies from the [Reuters-21578 collection at UCI](https://archive.ics.uci.edu/dataset/137/reuters+21578+text+categorization+collection). Save each selected body as a separate `.txt` file in `data/`. Run the program and compare its clusters with the articles' original categories. The categories are for your comparison; the clustering program does not read them.

## Code

```python
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
```

## Code explanation line by line

Line numbers refer to `practical6.py`.

| Line | What it does |
|---:|---|
| 1-3 | Import regular expressions, term counting, and file paths. |
| 5-7 | Import the stemmer, stop words, TF-IDF, and cosine similarity. |
| 9-11 | Set the data folder and similarity threshold; create the stemmer. |
| 14-16 | Define conflation: find lowercase words, remove stop words, and stem the rest. |
| 19-21 | Find text files, keep their names, read them, and conflate their text. |
| 23-24 | Print each document's term-frequency dictionary. |
| 26-27 | Convert the processed words into TF-IDF vectors. |
| 29 | Start empty lists for clusters and their leaders. |
| 30 | Visit documents in order, one at a time. |
| 31-34 | Make the first document the first cluster's leader. |
| 36-37 | Compare the current document with each leader and locate its best match. |
| 38-39 | Add it to the best cluster when similarity reaches the threshold. |
| 40-42 | Otherwise, start a new cluster led by this document. |
| 44-47 | Print each cluster, its leader, and its member filenames. |

## Viva questions with answers

1. **What is conflation in information retrieval?** It groups related word forms under one common form, making similar documents easier to match.
2. **What is a stop word?** A common word, such as “the” or “is,” that is often removed because it carries little search meaning.
3. **What does the Porter stemmer do?** It reduces words to stems, such as “connected” and “connecting” to “connect.”
4. **What does term frequency represent?** How many times each term occurs in a document.
5. **What is TF-IDF?** A weighting method that gives more importance to terms frequent in one document but less common across all documents.
6. **What does cosine similarity measure?** How similar two document vectors are; a higher score means they are more alike.
7. **How does single-pass clustering choose a cluster?** It compares a document with each current cluster leader and joins the closest cluster if the score reaches the threshold.
8. **What is a cluster leader?** The first document assigned to a cluster; later documents are compared with it.
9. **What happens when the similarity threshold increases?** Fewer documents meet the threshold, so more clusters are usually created.
10. **Why can document order change the result?** Each assignment uses the current leaders, and the leaders depend on which documents were processed first.