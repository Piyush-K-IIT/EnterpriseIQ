import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from the project root
load_dotenv(PROJECT_ROOT / ".env")

# Check whether the API key was loaded
api_key = os.getenv("GEMINI_API_KEY")

print("Gemini API key loaded:", bool(api_key))


# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=api_key
)


# Test the model
response = llm.invoke(
    "Explain what an API is in one sentence."
)

print("\nGemini Response:")
print(response.content)