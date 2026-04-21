from typing import List, Optional

from langchain_community.graphs.graph_document import (
    Node as BaseNode,
    Relationship as BaseRelationship
)
from pydantic import Field, BaseModel


class Node(BaseNode):
    properties: dict = Field(default_factory=dict, description="Node properties")


class Relationship(BaseRelationship):
    properties: dict = Field(default_factory=dict, description="Relationship properties")


class KnowledgeGraph(BaseModel):
    """Generate a knowledge graph with entities and relationships."""
    nodes: List[Node] = Field(
        ..., description="List of nodes in the knowledge graph")
    rels: List[Relationship] = Field(
        ..., description="List of relationships in the knowledge graph"
    )


def map_to_base_node(node: Node) -> BaseNode:
    """Map the KnowledgeGraph Node to the base Node."""
    properties = node.properties.copy() if node.properties else {}
    # Add name property for better Cypher statement generation
    if "name" not in properties:
        properties["name"] = node.id.title()
    return BaseNode(
        id=node.id.title(), type=node.type.capitalize(), properties=properties
    )


def map_to_base_relationship(rel: Relationship) -> BaseRelationship:
    """Map the KnowledgeGraph Relationship to the base Relationship."""
    source = map_to_base_node(rel.source)
    target = map_to_base_node(rel.target)
    properties = rel.properties.copy() if rel.properties else {}
    return BaseRelationship(
        source=source, target=target, type=rel.type, properties=properties
    )
