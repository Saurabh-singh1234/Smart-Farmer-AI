from PIL import Image
import google.generativeai as genai

import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_crop_image(image):

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    response = model.generate_content([
        "Analyze crop disease",
        image
    ])

    return response.text