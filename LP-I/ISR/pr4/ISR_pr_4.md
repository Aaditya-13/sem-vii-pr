# ISR Practical 4: Image Histogram and Basic CBIR

## Aim

Create sample images, display them, plot a color histogram, and demonstrate basic content-based image retrieval with ImageHash.

## How the code works

1. **Imports and folder:** OpenCV creates and reads images; NumPy builds pixel arrays; Matplotlib displays images and the histogram; Pillow and ImageHash calculate image hashes. The `images` folder is created if needed.
2. **Create samples:** The loop makes five 200Ã—200 solid-color images and draws a white circle on each. They are saved as `image1.jpg` through `image5.jpg`.
3. **Display samples:** Each image is loaded, converted from OpenCV's BGR color order to RGB for Matplotlib, and shown in a grid.
4. **Plot histogram:** The code loads `image1.jpg`, converts it to HSV, calculates a histogram for the hue channel, and plots it.
5. **CBIR with hashes:** The average hash of `image1.jpg` is the query. The code calculates a hash for each sample and prints the image if its hash distance from the query is below 15.

## Example

`query - h` is the Hamming distance between two hashes: a smaller value means the images look more alike to this hash method.

## Run

Install dependencies with `python -m pip install opencv-python numpy matplotlib ImageHash Pillow`, then run `python ISR_pr_4.py`.

## Limitations


## Code with explanation

### Create sample images

    os.makedirs("images", exist_ok=True)
    colors = [(255,0,0), (0,255,0), (0,0,255),
              (255,255,0), (255,0,255)]

    for i, color in enumerate(colors):
        img = np.zeros((200,200,3), dtype=np.uint8)
        img[:] = color
        cv2.circle(img, (100,100), 50, (255,255,255), -1)
        cv2.imwrite(f"images/image{i+1}.jpg", img)

The folder is created first. colors holds BGR background colors. zeros makes a 200 by 200 three-channel image; img[:] fills it. circle draws a filled white circle; -1 means fill it. imwrite saves each numbered image.

### Display images

    for i in range(5):
        img = cv2.imread(f"images/image{i+1}.jpg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(2,3,i+1)
        plt.imshow(img)
        plt.title(f"Image {i+1}")
        plt.axis("off")

imread loads each image. OpenCV uses BGR, so cvtColor converts it to RGB for Matplotlib. subplot selects a cell in the grid; imshow displays the image; title labels it; axis off hides axes. tight_layout adjusts spacing and show displays the figure.

### Plot the color histogram

    img = cv2.imread("images/image1.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0], None, [256], [0,256])

    plt.plot(hist)
    plt.title("Color Histogram")
    plt.show()

The image is converted to HSV. calcHist selects channel 0 (hue), uses 256 bins and the range 0 to 256. The result is plotted. This is a hue histogram only; there is no texture extraction. OpenCV hue normally uses a 0 to 180 range, so the chosen histogram range could be improved.

### Retrieve similar images with hashes

    query = imagehash.average_hash(Image.open("images/image1.jpg"))
    for i in range(5):
        path = f"images/image{i+1}.jpg"
        h = imagehash.average_hash(Image.open(path))
        if query - h < 15:
            print(f"Image {i+1} is similar")

image1 is the query. Each loop iteration makes a hash for another image. query - h is the Hamming distance, the number of differing hash bits. A distance below 15 is treated as similar. This reports matches; it does not rank them.

