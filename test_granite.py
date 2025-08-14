# test_granite.py
"""
Robust test for your Granite / HF-based rewrite function.

Behavior:
- Tries to import rewrite_with_hf from services.rewrite.
- If the import or HF API key is missing, falls back to a safe local stub.
- Prints the rewritten output or an error message for easy debugging.
"""

import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# Try to import the real function; if not available, provide a fallback stub.
try:
    from services.rewrite import rewrite_with_hf  # expected signature: (text, hf_key) -> str
    have_rewrite = True
except Exception as e:
    # Fallback stub
    have_rewrite = False

    def rewrite_with_hf(text, hf_key=None):
        # This is a simple placeholder to let the rest of your pipeline run
        # when you don't yet have a Granite/HF implementation.
        return f"[STUB - no HF key provided] {text}"


def main():
    sample = "Hello, this is a test."
    print("Loaded environment.")
    if HF_API_KEY:
        print("HF_API_KEY found in environment — will attempt to use the real rewrite_with_hf (if available).")
    else:
        print("Warning: HF_API_KEY not found in environment. Using local stub rewrite function.")

    try:
        # If real rewrite_with_hf requires only (text, hf_key) this will work.
        # If your real function signature differs, you'll replace it later when we update services/rewrite.py
        resp = rewrite_with_hf(sample, HF_API_KEY)
        print("Rewrite response:")
        print(resp)
    except Exception as exc:
        print("Error while calling rewrite_with_hf:", exc)


if __name__ == "__main__":
    main()
