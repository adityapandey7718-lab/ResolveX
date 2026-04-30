import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

with open("available_models.txt", "w") as f:
    try:
        f.write("Available Models:\n")
        for m in genai.list_models():
            f.write(f"{m.name} - {m.supported_generation_methods}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")
