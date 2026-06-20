import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PROMPT = """
You are an insurance claim reviewer.

Analyze the image and return ONLY JSON.

{
  "issue_type":"",
  "object_part":"",
  "severity":"",
  "damage_visible":true,
  "valid_image":true,
  "risk_flags":[]
}

Allowed issue_type:
dent, scratch, crack, glass_shatter,
broken_part, missing_part,
torn_packaging, crushed_packaging,
water_damage, stain, none, unknown

Severity:
none, low, medium, high, unknown
"""

def analyze_image(image_path):
    img = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[PROMPT, img]
    )

    return response.text


if __name__ == "__main__":
    image = "dataset/images/sample/case_001/img_1.jpg"

    print(analyze_image(image))