print("Importing AsyncHtmlLoader...")
try:
    from langchain_community.document_loaders import AsyncHtmlLoader
    print("AsyncHtmlLoader imported.")
except Exception as e:
    print(f"AsyncHtmlLoader failed: {e}")
