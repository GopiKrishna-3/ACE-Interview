import google.generativeai as genai
from app.config import Config
import traceback
import sys

print("Starting Gemini Test...")
try:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    print("API Key configured.")
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Model initialized. Calling generate_content...")
    response = model.generate_content("Say hello in JSON")
    print("Success! Response:")
    print(response.text)
except BaseException as e:
    print("Caught an exception!")
    print(f"Exception Type: {type(e)}")
    print(f"Exception Message: {str(e)}")
    traceback.print_exc(file=sys.stdout)
