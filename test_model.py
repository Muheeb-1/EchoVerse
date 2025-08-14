# test_model.py
"""
Safer Hugging Face model test.

Usage:
1. Create a .env file in the project root with:
   HF_API_KEY=REPLACE_WITH_YOUR_KEY
   HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.2  # optional

2. Run:
   python test_model.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2")
TEST_INPUT = os.getenv("TEST_INPUT", "Hello, how are you?")

if not HF_API_KEY:
    print("ERROR: HF_API_KEY not found in environment. Please add it to your .env file.")
    print("Example .env:")
    print("  HF_API_KEY=REPLACE_WITH_YOUR_KEY")
    print("  HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.2  # optional")
    sys.exit(1)

url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}
payload = {"inputs": TEST_INPUT}

print("Testing model:", HF_MODEL)
try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
except requests.exceptions.HTTPError as he:
    print("HTTP error while calling the model:", he)
    if resp is not None:
        print("Server response (first 2000 chars):")
        print(resp.text[:2000])
    sys.exit(1)
except requests.exceptions.RequestException as re:
    print("Network error while contacting Hugging Face API:", re)
    sys.exit(1)

print("STATUS:", resp.status_code)
print("RESPONSE (first 2000 chars):")
print(resp.text[:2000])
