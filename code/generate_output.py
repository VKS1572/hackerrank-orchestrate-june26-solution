import os
import re
import json
import time
import pandas as pd

from PIL import Image
from dotenv import load_dotenv
from google import genai

# =========================
# LOAD API KEY
# =========================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# LOAD DATA
# =========================

claims = pd.read_csv("dataset/claims.csv")

output_rows = []

# =========================
# PROCESS CLAIMS
# =========================

for idx, row in claims.iterrows():

    print(f"\nProcessing claim {idx + 1}/{len(claims)}")

    claim = row["user_claim"]
    claim_object = row["claim_object"]

    image_paths = [
        "dataset/" + p.strip()
        for p in row["image_paths"].split(";")
    ]

    prompt = f"""
You are an insurance damage claim reviewer.

User Claim:
{claim}

Claim Object:
{claim_object}

Analyze ALL attached images.

IMPORTANT:

Use ONLY these values.

claim_status:
supported
contradicted
not_enough_information

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

severity:
none
low
medium
high
unknown

Return ONLY valid JSON.

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

    contents = [prompt]

    try:

        for path in image_paths:
            contents.append(Image.open(path))

        response = None

        # Retry logic for 429 / 503
        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )

                break

            except Exception as e:

                print(f"Retry {attempt+1}/3")

                if attempt < 2:
                    time.sleep(15)
                else:
                    raise e

        text = response.text.strip()

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
        text = text.strip()

        result = json.loads(text)

    except Exception as e:

        print("ERROR:", e)

        result = {
            "evidence_standard_met": False,
            "evidence_standard_met_reason": "processing_error",
            "risk_flags": ["manual_review_required"],
            "issue_type": "unknown",
            "object_part": "unknown",
            "claim_status": "not_enough_information",
            "claim_status_justification": str(e),
            "supporting_image_ids": ["none"],
            "valid_image": False,
            "severity": "unknown"
        }

    # -----------------------
    # Fix Risk Flags
    # -----------------------

    risk_flags = result.get("risk_flags", ["none"])

    if not risk_flags:
        risk_flags = ["none"]

    # -----------------------
    # Fix Supporting IDs
    # -----------------------

    supporting_ids = result.get(
        "supporting_image_ids",
        ["none"]
    )

    if not supporting_ids:
        supporting_ids = ["none"]

    # -----------------------
    # Save Row
    # -----------------------

    output_rows.append({

        "user_id":
            row["user_id"],

        "image_paths":
            row["image_paths"],

        "user_claim":
            row["user_claim"],

        "claim_object":
            row["claim_object"],

        "evidence_standard_met":
            result.get(
                "evidence_standard_met",
                False
            ),

        "evidence_standard_met_reason":
            result.get(
                "evidence_standard_met_reason",
                ""
            ),

        "risk_flags":
            ";".join(risk_flags),

        "issue_type":
            result.get(
                "issue_type",
                "unknown"
            ),

        "object_part":
            result.get(
                "object_part",
                "unknown"
            ),

        "claim_status":
            result.get(
                "claim_status",
                "not_enough_information"
            ),

        "claim_status_justification":
            result.get(
                "claim_status_justification",
                ""
            ),

        "supporting_image_ids":
            ";".join(supporting_ids),

        "valid_image":
            result.get(
                "valid_image",
                False
            ),

        "severity":
            result.get(
                "severity",
                "unknown"
            )
    })

# =========================
# SAVE OUTPUT
# =========================

output_df = pd.DataFrame(output_rows)

output_df.to_csv(
    "final_output.csv",
    index=False
)

print("\nDone!")
print("Saved: final_output.csv")