from pathlib import Path
import cv2
import imagehash
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
from skimage.feature import graycomatrix, graycoprops

IMAGE_DIR = Path(__file__).parent / "images"
QUERY = IMAGE_DIR / "query.png"
TOP_K = 5

def extract_features(path):
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    color = cv2.normalize(color, color).flatten()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) // 32
    glcm = graycomatrix(gray, distances=[1], angles=[0], levels=8,
                        symmetric=True, normed=True)
    texture = np.array([graycoprops(glcm, name)[0, 0]
                        for name in ("contrast", "correlation", "energy", "homogeneity")])
    phash = imagehash.phash(Image.open(path))
    return color, texture, phash

query_color, query_texture, query_hash = extract_features(QUERY)
rows = []
for path in sorted(IMAGE_DIR.iterdir()):
    if path == QUERY or path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue
    color, texture, phash = extract_features(path)
    color_distance = cv2.compareHist(query_color, color, cv2.HISTCMP_BHATTACHARYYA)
    texture_distance = float(np.mean(np.abs(query_texture - texture) /
                                     np.maximum(np.abs(query_texture), 1)))
    hash_distance = (query_hash - phash) / 64
    rows.append({"image": path.name, "color": color_distance,
                 "texture": texture_distance, "hash": hash_distance})

# Normalize texture differences and combine the three distances with assignment weights.
if not rows:
    raise ValueError("Add sample images beside query.png in the images folder.")
max_texture = max(row["texture"] for row in rows) or 1
for row in rows:
    row["texture"] /= max_texture
    row["score"] = 0.50 * row["color"] + 0.20 * row["texture"] + 0.30 * row["hash"]
results = sorted(rows, key=lambda row: row["score"])
print("Top similar images for", QUERY.name)
for rank, row in enumerate(results[:TOP_K], 1):
    print(rank, row["image"], "score:", round(row["score"], 3))
pd.DataFrame(results).to_csv(Path(__file__).parent / "results.csv", index=False)

hist = cv2.calcHist([cv2.cvtColor(cv2.imread(str(QUERY)), cv2.COLOR_BGR2HSV)],
                    [0], None, [32], [0, 180]).flatten()
px.bar(x=list(range(32)), y=hist, labels={"x": "Hue bin", "y": "Pixel count"},
       title="Query image hue histogram").show()
