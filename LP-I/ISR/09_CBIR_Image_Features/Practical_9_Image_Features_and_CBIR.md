# Practical 9 Image Features and CBIR

## Aim

Extract simple color and texture features from images, plot a feature histogram, and retrieve images similar to a query using OpenCV and ImageHash.

## Theory

A color histogram counts pixel colors. This practical uses a histogram of the HSV hue channel. As a simple texture measure, it uses the standard deviation of grayscale pixel values. Perceptual hash (pHash) creates a compact image fingerprint; the Hamming distance between hashes is smaller for more similar images.

The program adds normalized color, texture, and hash distances, then ranks images from the smallest distance to the largest. It also plots the query's hue histogram and displays the retrieved images.

## Files and run

- `practical9.py` reads images from `images/` and uses `query.png` as the search image.
- `Practical_9.ipynb` runs the same steps in notebook cells.
- `images/` contains a query and four simple sample images. Replace or add PNG images to try your own set.

Install the libraries once:

```bash
python -m pip install opencv-python ImageHash Pillow matplotlib
```

From this practical's folder run:

```bash
python practical9.py
```

For Jupyter, open `Practical_9.ipynb` with this practical folder as the working directory, then run cells from top to bottom.

## Code

```python
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
```

## Code explanation line by line

Line numbers refer to `practical9.py`.

| Line | Explanation |
|---:|---|
| 1-6 | Import path handling, OpenCV, ImageHash, plotting, and image loading. |
| 8-10 | Choose the image folder, query image, and number of results. |
| 13-21 | Read an image and extract its hue histogram, grayscale texture value, and pHash. |
| 24 | Extract the three features from the query image. |
| 25-29 | Read each other PNG image and extract its features. |
| 30-33 | Compare color, texture, and hashes, then combine the normalized distances. |
| 35-38 | Sort by distance and print the closest images. Smaller distance means more similar. |
| 40-44 | Plot the query image's hue histogram. |
| 46-53 | Display the query image beside the top retrieved images. |

## Related applications

- **Spotify-style music discovery:** audio features can help find tracks with similar sound. The example uses the same retrieval idea, but image features do not analyze music.
- **YouTube-style video retrieval:** visual features from video frames or thumbnails can help find visually similar content.

## Viva questions with answers

1. **What is CBIR?** Content-Based Image Retrieval finds images by comparing their visual features.
2. **What is a color histogram?** A count of how many pixels fall into each color range.
3. **What does HSV stand for?** Hue, Saturation, and Value.
4. **What texture feature is extracted here?** The standard deviation of grayscale pixel values, used as a simple measure of image variation.
5. **What is a perceptual hash?** A compact fingerprint designed to represent an image's visual structure.
6. **What does hash distance tell us?** The number of differing hash bits; smaller distance usually means more similar images.
7. **Why sort distances from smallest to largest?** Smaller feature distance indicates a closer match to the query.
8. **What does the histogram plot show?** The distribution of hue values in the query image.
9. **Name one video retrieval use case.** Finding visually similar video frames or thumbnails.
10. **How can music search use a similar idea?** It can compare audio features to find tracks with similar sound, using audio rather than image features.
