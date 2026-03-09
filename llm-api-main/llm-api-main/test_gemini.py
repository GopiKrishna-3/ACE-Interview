import google.generativeai as genai
from app.config import Config
import json

genai.configure(api_key=Config.GEMINI_API_KEY)

try:
    print(f"Testing Gemini API with Key: {Config.GEMINI_API_KEY[:5]}...{Config.GEMINI_API_KEY[-5:]}")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say hello world in json format: {'message': '...'}")
    print("API Call Successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"API Call Failed!")
    print(f"Error: {e}")
