# ISR Practical 3: Information Retrieval Evaluation and A/B Testing

## Aim

Calculate Precision, Recall, F-measure, E-measure, and NDCG for a sample query, then demonstrate a basic A/B test.

## How the code works

1. **Create files:** The code creates a `documents` folder and writes five short sample documents into it.
2. **Choose query and relevance labels:** The query is `Python programming`. The `relevant` list is a hand-written set of documents judged relevant for this example.
3. **Retrieve documents:** Each file is read and split into words. If it contains either query word, it is added to `results`.
4. **Calculate metrics:**
   - Precision = relevant retrieved / all retrieved.
   - Recall = relevant retrieved / all known relevant.
   - F-measure combines precision and recall.
   - E-measure is calculated here as `1 - F`.
   - NDCG uses binary relevance scores and discounts results lower in the list.
5. **Simulate A/B testing:** With a fixed random seed, the code simulates 2,000 users for version A (10% click chance) and version B (12% click chance), then calculates a z-score and p-value to check whether the click-through difference is significant.
6. **Print overview:** It prints a short A/B explanation and example areas where search interfaces may be evaluated.

## Example

If four documents are retrieved and three are marked relevant, precision is `3/4 = 0.75`. If all three known relevant documents were retrieved, recall is `3/3 = 1.0`.

## Run

This script uses Python's standard library only. Run `python ISR_pr_3.py`.

## Important limitation


## Code with explanation

### Create sample files

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

The folder is created first. docs maps filenames to text. The loop writes each text to a file, creating this practical's sample dataset.

### Query and retrieval

    query = "Python programming"
    relevant = ["D1.txt", "D2.txt", "D4.txt"]
    results = []

    for name in docs:
        text = open("documents/" + name).read().lower().split()
        if any(w in text for w in query.lower().split()):
            results.append(name)

relevant is the hand-entered set of relevant documents. Each file is read, lowercased, and split into words. any checks whether at least one query term appears. Matching filenames are added to results. This retrieval is not ranked.

### Precision, recall, F and E

    TP = len(set(results) & set(relevant))
    P = TP / len(results) if results else 0
    R = TP / len(relevant) if relevant else 0
    F = 2 * P * R / (P + R) if P + R else 0
    E = 1 - F

The set intersection counts retrieved documents that are relevant. P is precision, relevant retrieved divided by all retrieved. R is recall, relevant retrieved divided by all relevant. The conditional expressions prevent division by zero. F is the harmonic mean of P and R. E is defined here as 1-F.

### NDCG

    scores = [1 if d in relevant else 0 for d in results]
    dcg = sum(s / math.log2(i + 2) for i, s in enumerate(scores))
    idcg = sum(s / math.log2(i + 2)
               for i, s in enumerate(sorted(scores, reverse=True)))
    ndcg = dcg / idcg if idcg else 0

scores marks each retrieved document relevant (1) or not (0). DCG discounts relevant results lower in the list. IDCG uses the ideal ordering with relevant results first. NDCG divides actual DCG by ideal DCG, with a guard for zero.

### A/B test simulation

    random.seed(1)
    n = 2000
    cA = sum(random.random() < 0.10 for _ in range(n))
    cB = sum(random.random() < 0.12 for _ in range(n))

The fixed seed makes the simulation repeatable. Each version has 2,000 simulated users. The comparisons simulate a 10% click chance for A and 12% for B; cA and cB count clicks.

    pA, pB = cA/n, cB/n
    pool = (cA + cB) / (2*n)
    z = (pB-pA) / math.sqrt(pool*(1-pool)*(2/n))
    pval = math.erfc(abs(z)/math.sqrt(2))

pA and pB are click rates. pool is the combined rate. z measures the difference relative to estimated variation. pval converts z into a two-sided p-value. The following condition says B improved only if p is below 0.05 and B's rate is higher.

