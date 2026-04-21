try:
    from langchain.schema import Document
    print("Found langchain.schema.Document")
except ImportError:
    try:
        from langchain_core.documents import Document
        print("Found langchain_core.documents.Document")
    except ImportError:
        print("Document not found")
