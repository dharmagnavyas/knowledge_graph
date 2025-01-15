from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    """Configuration for the Knowledge Graph Generator"""
    pdf_input_dir: str
    falkordb_host: str = "localhost"
    falkordb_port: int = 6379
    batch_size: int = 5
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200

config = Config(
    pdf_input_dir="./data/pdfs",
)
