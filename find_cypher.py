try:
    from langchain.chains import GraphCypherQAChain
    print("Found in langchain.chains")
except ImportError:
    pass

try:
    from langchain_community.chains import GraphCypherQAChain
    print("Found in langchain_community.chains")
except ImportError:
    pass

try:
    from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
    print("Found in langchain_community.chains.graph_qa.cypher")
except ImportError:
    pass
