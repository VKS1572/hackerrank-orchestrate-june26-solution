import os
from google import genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

img = Image.open("dataset/images/sample/case_001/img_1.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Describe what damage is visible in this image. Mention object, damaged part, issue type and severity.",
        img
    ]
)

print(response.text)