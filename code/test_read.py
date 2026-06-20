import pandas as pd

claims = pd.read_csv("dataset/claims.csv")

print("Total Claims:", len(claims))
print("\nColumns:")
print(claims.columns.tolist())

print("\nFirst Row:")
print(claims.iloc[0])