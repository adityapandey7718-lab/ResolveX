import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"Testing with API Key: {api_key[:5]}...{api_key[-5:]}")

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello, say 'API is working'")
    print(f"Response: {response.text}")
    
    print("Testing Embedding...")
    emb = genai.embed_content(model="models/embedding-001", content="Hello world")
    print("Embedding successful")
    
except Exception as e:
    print(f"API TEST FAILED: {e}")
