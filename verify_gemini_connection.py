import os
import sys
from dotenv import load_dotenv

# Add src to path so we can import app modules
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app.llm import Llm

def verify():
    # load_dotenv() # Not strictly needed for key anymore
    print("Using hardcoded API Key...")
    
    try:
        print("Initializing Llm with Gemini (default hardcoded)...")
        llm = Llm(model="gemini-2.5-flash") # or leave empty to use default
        
        print("Testing extraction with a simple sentence...")
        input_text = "Google announced Project Gemini in California on December 6, 2023. It aims to revolutionize AI."
        # Note: This relies on the schema.yml being present and valid.
        try:
            result = llm.run(input_text)
            print("Result:", result)
            print("Verification SUCCESS!")
        except Exception as e:
            print("Extraction failed:", e)
            print("This might be due to schema or chain issues. Let's try direct generation to confirm connection.")
            try:
                msg = llm.llm.invoke("Hello, are you working?")
                print("Direct generation result:", msg.content)
                print("Connection SUCCESS (but extraction failed).")
            except Exception as e2:
                print("Direct generation failed:", e2)

    except Exception as e:
        print("Initialization failed:", e)

if __name__ == "__main__":
    verify()
