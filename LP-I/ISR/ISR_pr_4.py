
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import imagehash
from PIL import Image

os.makedirs("images", exist_ok=True)

# Create 5 sample images
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]

for i, color in enumerate(colors):
    img = np.zeros((200,200,3), dtype=np.uint8)
    img[:] = color
    cv2.circle(img, (100,100), 50, (255,255,255), -1)
    cv2.imwrite(f"images/image{i+1}.jpg", img)

print("Images created successfully!")

# Display images in tile format
plt.figure(figsize=(10,6))

for i in range(5):
    img = cv2.imread(f"images/image{i+1}.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(2,3,i+1)
    plt.imshow(img)
    plt.title(f"Image {i+1}")
    plt.axis("off")

plt.tight_layout()
plt.show()

# Color histogram
img = cv2.imread("images/image1.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hist = cv2.calcHist([hsv], [0], None, [256], [0,256])

plt.plot(hist)
plt.title("Color Histogram")
plt.show()

# CBIR using ImageHash
query = imagehash.average_hash(Image.open("images/image1.jpg"))

print("Similar Images:")

for i in range(5):
    path = f"images/image{i+1}.jpg"
    h = imagehash.average_hash(Image.open(path))

    if query - h < 15:
        print(f"Image {i+1} is similar")
