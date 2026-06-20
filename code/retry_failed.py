import os
import re
import json
import pandas as pd

from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

df = pd.read_csv("final_output.csv")

failed_rows = df[
    df["evidence_standard_met_reason"] == "processing_error"
]

print("Failed rows:", len(failed_rows))

for idx in failed_rows.index:

    print(f"\nReprocessing row {idx}")

    claim = df.loc[idx, "user_claim"]
    claim_object = df.loc[idx, "claim_object"]

    image_paths = [
        "dataset/" + p.strip()
        for p in df.loc[idx, "image_paths"].split(";")
    ]

    prompt = f"""
You are an insurance damage claim reviewer.

User Claim:
{claim}

Claim Object:
{claim_object}

Analyze ALL attached images.

Return ONLY valid JSON.

Allowed claim_status:
supported
contradicted
not_enough_information

Allowed issue_type:
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

Car object_part:
front_bumper
rear_bumper
door
hood
windshield
side_mirror
headlight
taillight
fender
quarter_panel
body
unknown

Laptop object_part:
screen
keyboard
trackpad
hinge
lid
corner
port
base
body
unknown

Package object_part:
box
package_corner
package_side
seal
label
contents
item
unknown

Severity:
none
low
medium
high
unknown

Return ONLY JSON:

{{
  "evidence_standard_met": true,
  "evidence_standard_met_reason": "",
  "risk_flags": ["none"],
  "issue_type": "",
  "object_part": "",
  "claim_status": "",
  "claim_status_justification": "",
  "supporting_image_ids": ["img_1"],
  "valid_image": true,
  "severity": ""
}}
"""

    try:

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

        result = json.loads(text)

        df.loc[idx, "evidence_standard_met"] = result.get(
            "evidence_standard_met", False
        )
        df.loc[idx, "evidence_standard_met_reason"] = result.get(
            "evidence_standard_met_reason", ""
        )
        df.loc[idx, "risk_flags"] = ";".join(
            result.get("risk_flags", ["none"])
        )
        df.loc[idx, "issue_type"] = result.get(
            "issue_type", "unknown"
        )
        df.loc[idx, "object_part"] = result.get(
            "object_part", "unknown"
        )
        df.loc[idx, "claim_status"] = result.get(
            "claim_status",
            "not_enough_information"
        )
        df.loc[idx, "claim_status_justification"] = result.get(
            "claim_status_justification",
            ""
        )
        df.loc[idx, "supporting_image_ids"] = ";".join(
            result.get("supporting_image_ids", [])
        )
        df.loc[idx, "valid_image"] = result.get(
            "valid_image", False
        )
        df.loc[idx, "severity"] = result.get(
            "severity", "unknown"
        )

        print("✓ Success")

    except Exception as e:
        print("ERROR:", e)

df.to_csv("final_output.csv", index=False)

print("\nDone!")
print("Updated final_output.csv")