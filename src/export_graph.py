# src/export_graph.py
import json
import redis
from pathlib import Path

def export_knowledge_graph(output_file: str = "knowledge_graph_export.json"):
    # Connect to Redis
    redis_conn = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Get all data
    export_data = {
        "processed_files": list(redis_conn.smembers("processed_files")),
        "nodes": {},
        "edges": []
    }
    
    # Get all nodes
    node_keys = redis_conn.keys("node:*")
    for node_key in node_keys:
        node_data = redis_conn.hgetall(node_key)
        node_id = node_key.split(":")[-1]
        export_data["nodes"][node_id] = node_data
    
    # Get all edges
    edge_keys = redis_conn.keys("edge:*")
    for edge_key in edge_keys:
        edge_data = redis_conn.hgetall(edge_key)
        export_data["edges"].append(edge_data)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"Knowledge graph exported to {output_file}")
    print(f"Total nodes: {len(export_data['nodes'])}")
    print(f"Total edges: {len(export_data['edges'])}")
    print(f"Processed files: {len(export_data['processed_files'])}")

if __name__ == "__main__":
    export_knowledge_graph()