from pathlib import Path

import cv2
import imagehash
import matplotlib.pyplot as plt
from PIL import Image

IMAGE_DIR = Path(__file__).parent / "images"
QUERY = IMAGE_DIR / "query.png"
TOP_K = 3


def features(path):
    image = cv2.imread(str(path))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    color_hist = cv2.calcHist([hsv], [0], None, [16], [0, 180])
    color_hist = cv2.normalize(color_hist, color_hist).flatten()
    texture = gray.std()
    image_hash = imagehash.phash(Image.open(path))
    return color_hist, texture, image_hash


query_hist, query_texture, query_hash = features(QUERY)
results = []
for path in sorted(IMAGE_DIR.glob("*.png")):
    if path.name == QUERY.name:
        continue
    hist, texture, image_hash = features(path)
    color_distance = cv2.compareHist(query_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
    texture_distance = abs(query_texture - texture) / 255
    hash_distance = (query_hash - image_hash) / 64
    results.append((color_distance + texture_distance + hash_distance, path))

results.sort(key=lambda result: result[0])
print("Most similar images:")
for rank, (distance, path) in enumerate(results[:TOP_K], start=1):
    print(rank, path.name, round(distance, 3))

plt.plot(query_hist)
plt.title("Query image color histogram")
plt.xlabel("Hue bin")
plt.ylabel("Frequency")
plt.show()

fig, axes = plt.subplots(1, TOP_K + 1, figsize=(12, 3))
for axis, (title, path) in zip(
        axes, [("Query", QUERY)] + [(p.name, p) for score, p in results[:TOP_K]]):
    image = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
    axis.imshow(image)
    axis.set_title(title)
    axis.axis("off")
plt.show()
