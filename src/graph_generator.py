from typing import List, Dict
import torch
from sentence_transformers import SentenceTransformer
import networkx as nx
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Node:
    id: str
    content: str
    embedding: torch.Tensor
    metadata: Dict

@dataclass
class Edge:
    source: str
    target: str
    weight: float

class KnowledgeGraphGenerator:
    """Generates Knowledge Graph from processed PDF content"""
    
    def __init__(self, embedding_model: str, chunk_size: int, chunk_overlap: int):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.graph = nx.DiGraph()
        
    def generate_embeddings(self, text: str) -> torch.Tensor:
        """Generate embeddings for text using the selected model"""
        return self.embedding_model.encode(text, convert_to_tensor=True)
        
    def create_nodes(self, elements: List[Dict]) -> List[Node]:
        """Create nodes from PDF elements"""
        nodes = []
        for element in elements:
            if element.get("text"):
                embedding = self.generate_embeddings(element["text"])
                node = Node(
                    id=element["element_id"],
                    content=element["text"],
                    embedding=embedding,
                    metadata={
                        "type": element.get("type", "text"),
                        "page_number": element.get("page_number", 0)
                    }
                )
                nodes.append(node)
        return nodes
        
    def create_edges(self, nodes: List[Node]) -> List[Edge]:
        """Create edges between related nodes based on similarity"""
        edges = []
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                similarity = torch.cosine_similarity(
                    node1.embedding.unsqueeze(0),
                    node2.embedding.unsqueeze(0)
                ).item()
                
                if similarity > 0.7:  # Threshold for creating an edge
                    edge = Edge(
                        source=node1.id,
                        target=node2.id,
                        weight=similarity
                    )
                    edges.append(edge)
        return edges
        
    def update_graph(self, nodes: List[Node], edges: List[Edge]):
        """Update the knowledge graph with new nodes and edges"""
        for node in nodes:
            self.graph.add_node(
                node.id,
                content=node.content,
                embedding=node.embedding.tolist(),  # Convert tensor to list for storage
                metadata=node.metadata
            )
            
        for edge in edges:
            self.graph.add_edge(
                edge.source,
                edge.target,
                weight=edge.weight
            )