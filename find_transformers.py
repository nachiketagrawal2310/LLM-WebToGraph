try:
    from langchain_community.document_transformers import BeautifulSoupTransformer
    print("Found in langchain_community.document_transformers")
except ImportError:
    print("Not found in langchain_community.document_transformers")

try:
    from langchain.document_transformers import BeautifulSoupTransformer
    print("Found in langchain.document_transformers")
except ImportError:
    pass
