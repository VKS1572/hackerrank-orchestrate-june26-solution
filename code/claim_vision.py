import os
import re
import pandas as pd

from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

claims = pd.read_csv("dataset/claims.csv")

for i in range(3):

    row = claims.iloc[i]

    claim = row["user_claim"]
    claim_object = row["claim_object"]

    image_paths = [
        "dataset/" + p
        for p in row["image_paths"].split(";")
    ]

    prompt = f"""
You are an insurance claim reviewer.

User Claim:
{claim}

Object:
{claim_object}

Analyze ALL attached images.

Use ONLY these values:

issue_type:
dent
scratch
crack
glass_shatter
broken_part
missing_part
torn_packaging
crushed_packaging
water_damage
stain
none
unknown

claim_status:
supported
contradicted
not_enough_information

severity:
none
low
medium
high
unknown

Return ONLY JSON.

{{
  "issue_type":"",
  "object_part":"",
  "claim_status":"",
  "severity":"",
  "justification":""
}}
"""

    contents = [prompt]

    for path in image_paths:
        contents.append(Image.open(path))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    text = response.text.strip()

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    print("\n" + "=" * 60)
    print(f"CLAIM {i+1}")
    print(text)