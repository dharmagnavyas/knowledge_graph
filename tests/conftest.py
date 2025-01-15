# tests/conftest.py
import pytest
from pathlib import Path
import torch
from src.config import Config
from src.pdf_processor import PDFProcessor
from src.graph_generator import KnowledgeGraphGenerator
from src.database import FalkorDBClient

@pytest.fixture
def test_config():
    return Config(
        pdf_input_dir="tests/data/pdfs",
        falkordb_host="localhost",
        falkordb_port=6379,
        batch_size=2,
        chunk_size=500,
        chunk_overlap=100
    )

@pytest.fixture
def sample_pdf_content():
    return [
        {
            "element_id": "1",
            "text": "This is a sample text from the first page.",
            "type": "paragraph",
            "page_number": 1
        },
        {
            "element_id": "2",
            "text": "This is related content from the second page.",
            "type": "paragraph",
            "page_number": 2
        }
    ]

@pytest.fixture
def mock_embeddings():
    return torch.tensor([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
