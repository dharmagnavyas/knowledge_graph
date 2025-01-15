import redis
import json
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class FalkorDBClient:
    """Handles interactions with Redis database"""
    
    def __init__(self, host: str, port: int):
        self.redis_conn = redis.Redis(host=host, port=port, decode_responses=True)
        self.graph_name = "knowledge_graph"
        
    def store_node(self, node_id: str, properties: Dict):
        """Store a node in Redis"""
        try:
            # Store node properties
            node_key = f"node:{node_id}"
            self.redis_conn.hset(node_key, mapping={
                "id": node_id,
                **properties,
                "embedding": json.dumps(properties.get("embedding", []))  # Convert embedding to JSON
            })
            
            # Add to processed files set if filename exists
            if "filename" in properties:
                self.redis_conn.sadd("processed_files", properties["filename"])
                
            logger.info(f"Stored node: {node_id}")
        except Exception as e:
            logger.error(f"Error storing node {node_id}: {str(e)}")
            raise
            
    def store_edge(self, source_id: str, target_id: str, properties: Dict):
        """Store an edge in Redis"""
        try:
            edge_key = f"edge:{source_id}:{target_id}"
            self.redis_conn.hset(edge_key, mapping={
                "source": source_id,
                "target": target_id,
                **properties
            })
            
            # Add to edge index for both nodes
            self.redis_conn.sadd(f"edges:from:{source_id}", edge_key)
            self.redis_conn.sadd(f"edges:to:{target_id}", edge_key)
            
            logger.info(f"Stored edge: {source_id} -> {target_id}")
        except Exception as e:
            logger.error(f"Error storing edge {source_id}->{target_id}: {str(e)}")
            raise
            
    def get_processed_files(self) -> List[str]:
        """Get list of already processed PDF files"""
        try:
            return list(self.redis_conn.smembers("processed_files"))
        except Exception as e:
            logger.error(f"Error getting processed files: {str(e)}")
            return []
            
    def get_node(self, node_id: str) -> Dict:
        """Retrieve a node from Redis"""
        node_key = f"node:{node_id}"
        node_data = self.redis_conn.hgetall(node_key)
        if node_data:
            node_data["embedding"] = json.loads(node_data.get("embedding", "[]"))
        return node_data
        
    def get_node_edges(self, node_id: str) -> List[Dict]:
        """Get all edges connected to a node"""
        edges = []
        # Get outgoing edges
        outgoing = self.redis_conn.smembers(f"edges:from:{node_id}")
        for edge_key in outgoing:
            edge_data = self.redis_conn.hgetall(edge_key)
            if edge_data:
                edges.append(edge_data)
                
        # Get incoming edges
        incoming = self.redis_conn.smembers(f"edges:to:{node_id}")
        for edge_key in incoming:
            edge_data = self.redis_conn.hgetall(edge_key)
            if edge_data:
                edges.append(edge_data)
                
        return edges
        
    def commit(self):
        """Ensure all data is written to Redis"""
        pass  # Redis performs writes immediately, no explicit commit needed