print("Importing BeautifulSoupTransformer...")
try:
    from langchain_community.document_transformers import BeautifulSoupTransformer
    print("BeautifulSoupTransformer imported.")
except Exception as e:
    print(f"BeautifulSoupTransformer failed: {e}")

print("Importing CSVLoader...")
try:
    from langchain_community.document_loaders import CSVLoader
    print("CSVLoader imported.")
except Exception as e:
    print(f"CSVLoader failed: {e}")
