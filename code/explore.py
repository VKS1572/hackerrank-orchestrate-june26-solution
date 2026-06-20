import pandas as pd

claims = pd.read_csv("dataset/claims.csv")

for i in range(5):
    print("\n====================")
    print("ROW:", i)
    print("OBJECT:", claims.iloc[i]["claim_object"])
    print("CLAIM:")
    print(claims.iloc[i]["user_claim"])