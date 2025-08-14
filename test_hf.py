# test_hf.py — safer Hugging Face token + model test
"""
Usage:
- Put your HF_API_KEY and optional HF_MODEL_ID in a .env file at project root:
    HF_API_KEY=REPLACE_WITH_YOUR_KEY
    HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.2

- Run:
    python test_hf.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2")

if not HF_API_KEY:
    print("ERROR: HF_API_KEY not found in environment. Please add it to your .env file.")
    print("Example .env contents:")
    print("  HF_API_KEY=REPLACE_WITH_YOUR_KEY")
    print("  HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.2  # optional")
    sys.exit(1)

url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}
payload = {"inputs": "Hello, how are you?"}

print("Testing model:", HF_MODEL)
try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
except requests.exceptions.HTTPError as he:
    print("HTTP error while calling the model:", he)
    if resp is not None:
        # show server response body for debugging (truncated)
        print("Server response (first 2000 chars):")
        print(resp.text[:2000])
    sys.exit(1)
except requests.exceptions.RequestException as re:
    print("Network error while contacting Hugging Face API:", re)
    sys.exit(1)

print("STATUS:", resp.status_code)
print("RESPONSE (first 2000 chars):")
print(resp.text[:2000])
