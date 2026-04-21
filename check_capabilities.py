from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

def check():
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv('GOOGLE_API_KEY'))
        if hasattr(llm, 'with_structured_output'):
            print("with_structured_output is AVAILABLE")
        else:
            print("with_structured_output is NOT available")
            
        # Also check imports
        try:
            from langchain.chains import create_extraction_chain
            print("create_extraction_chain IMPORTABLE")
        except ImportError:
            print("create_extraction_chain NOT IMPORTABLE")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
