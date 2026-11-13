# ISR Practical 1: Conflation and Single-Pass Clustering

## Aim

Stem five sample documents, create TF-IDF document representations, and group similar documents with a simple single-pass clustering method.

## How the code works

1. **Imports:** NLTK provides `PorterStemmer`; scikit-learn provides TF-IDF and cosine similarity.
2. **Sample documents:** `docs` contains five short, hardcoded text documents.
3. **Conflation:** Each document is lowercased, split into words, and stemmed. The words are joined back into a document. For example, `announces economic policies` becomes approximately `announc econom polici`.
4. **TF-IDF:** `fit_transform(docs)` turns the documents into weighted term vectors. `X.toarray().round(2)` prints the values rounded to two decimals.
5. **Single-pass clustering:** `clusters` stores groups of document indexes; `leaders` stores the first document in each group. Each new document is compared with leaders in order. If cosine similarity reaches `0.20`, it joins the first matching cluster. If none match, it starts a new cluster and becomes that cluster's leader.
6. **Display:** The code prints document numbers starting from 1, although Python indexes them starting from 0.

## Small clustering example

If document 2 is similar enough to document 1, it joins document 1's cluster. If it does not match any existing leader, it starts a new cluster.

## Run

Install dependencies with `python -m pip install nltk scikit-learn`, then run `python ISR_pr_1.py`.

## Notes


## Code with explanation

### Imports and input documents

    from nltk.stem import PorterStemmer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    docs = [
        "Government announces economic policies",
        "Government supports economic growth",
        "Artificial intelligence changes technology",
        "Technology uses artificial intelligence",
        "Cricket players play matches"
    ]

PorterStemmer reduces words to stems. TfidfVectorizer turns the texts into numeric term vectors. cosine_similarity compares those vectors. The list is the five sample input documents.

### Conflation

    stemmer = PorterStemmer()

    docs = [
        " ".join(stemmer.stem(word) for word in doc.lower().split())
        for doc in docs
    ]

The stemmer is created once. The outer for goes through each document. lower makes it lowercase; split separates words. The inner for stems each word. join puts the stemmed words back into one string. This new list replaces docs. For example, policies becomes polici.

### TF-IDF representation

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)
    print(X.toarray().round(2))

fit_transform learns the vocabulary and creates a TF-IDF vector for every document. X is sparse to save space. toarray displays a regular matrix and round(2) limits decimals.

### Single-pass clustering

    clusters = []
    leaders = []
    threshold = 0.20

    for i in range(len(docs)):
        added = False
        for c, leader in enumerate(leaders):
            similarity = cosine_similarity(X[i], X[leader])[0][0]
            if similarity >= threshold:
                clusters[c].append(i)
                added = True
                break
        if not added:
            clusters.append([i])
            leaders.append(i)

clusters stores groups of document indexes. leaders stores the first document in each group. The outer loop considers documents one at a time. added starts False. The inner loop compares the current document with each leader. [0][0] extracts the single similarity number from cosine_similarity's result. If it reaches 0.20, the document joins that cluster and break stops checking. If no leader matches, a new cluster is created and this document becomes its leader. This version takes the first qualifying cluster.

### Display

    for i, cluster in enumerate(clusters):
        print("Cluster", i + 1, ":", [document + 1 for document in cluster])

Python indexes begin at zero. Adding one makes the printed document numbers start at 1. For example, index 0 displays as document 1.

