import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyBt8hNgFnkNlm5UHy3pHdPjMPyI44ZLbTw')

try:
    print("Listing models...")
    for m in genai.list_models():
        print(f"Model: {m.name}, Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
