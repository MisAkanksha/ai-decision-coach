from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Fetch API key
api_key = os.getenv("OPENAI_API_KEY")

# Print test result
if api_key:
    print("✅ API Key Loaded Successfully!")
else:
    print("❌ API Key NOT Found. Check .env file.")
