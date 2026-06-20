import pandas as pd
from PIL import Image

claims = pd.read_csv("dataset/claims.csv")

row = claims.iloc[0]

image_paths = []

for p in row["image_paths"].split(";"):
    image_paths.append("dataset/" + p)

for path in image_paths:
    img = Image.open(path)
    print("Loaded:", path)