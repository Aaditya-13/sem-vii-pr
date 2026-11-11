# Assignment 5 ? CBIR image features

## How to run

Install with `python -m pip install opencv-python imagehash pillow plotly scikit-image numpy pandas`, then run `python practical5.py`. Put images in `images/` and set the query as `query.png`. The program extracts a 2-D HSV histogram, GLCM contrast/correlation/energy/homogeneity and perceptual hash, ranks the top five with the assignment weights 0.50/0.20/0.30, opens a Plotly hue histogram and writes `results.csv`. Notebook: `Practical.ipynb`.
