from pathlib import Path
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

DATA = Path(__file__).parent / "data" / "document.txt"
text = DATA.read_text(encoding="utf-8")
words = [w for w in word_tokenize(text.lower())
         if w.isalnum() and w not in set(stopwords.words("english"))]
stemmer = PorterStemmer()
conflated = [stemmer.stem(w) for w in words]
lemmatized = [WordNetLemmatizer().lemmatize(w) for w in words]
representation = Counter(conflated)

print("Original text:\n", text)
print("\nAfter stop-word removal:", words)
print("\nConflated (stemmed) terms:", conflated)
print("\nLemmatized terms:", lemmatized)
print("\nDocument representation (term frequency):", dict(representation))
