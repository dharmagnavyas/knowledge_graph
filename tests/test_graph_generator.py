import pytest
import torch
from src.graph_generator import KnowledgeGraphGenerator

def test_graph_generator_initialization(test_config):
    generator = KnowledgeGraphGenerator(
        test_config.embedding_model,
        test_config.chunk_size,
        test_config.chunk_overlap
    )
    assert generator.chunk_size == test_config.chunk_size
    assert generator.chunk_overlap == test_config.chunk_overlap

def test_generate_embeddings(test_config):
    generator = KnowledgeGraphGenerator(
        test_config.embedding_model,
        test_config.chunk_size,
        test_config.chunk_overlap
    )
    text = "Test content for embedding generation"
    embedding = generator.generate_embeddings(text)
    assert isinstance(embedding, torch.Tensor)
    assert embedding.dim() == 1

def test_create_nodes(test_config, sample_pdf_content, mocker):
    generator = KnowledgeGraphGenerator(
        test_config.embedding_model,
        test_config.chunk_size,
        test_config.chunk_overlap
    )
    
    # Mock embedding generation
    mocker.patch.object(
        generator,
        'generate_embeddings',
        return_value=torch.tensor([0.1, 0.2, 0.3])
    )
    
    nodes = generator.create_nodes(sample_pdf_content)
    assert len(nodes) == len(sample_pdf_content)
    assert nodes[0].content == sample_pdf_content[0]["text"]

def test_create_edges(test_config, mock_embeddings):
    generator = KnowledgeGraphGenerator(
        test_config.embedding_model,
        test_config.chunk_size,
        test_config.chunk_overlap
    )
    
    # Create test nodes with mock embeddings
    nodes = [
        Node("1", "content1", mock_embeddings[0], {}),
        Node("2", "content2", mock_embeddings[1], {})
    ]
    
    edges = generator.create_edges(nodes)
    assert isinstance(edges, list)
    if edges:  # If similarity threshold was met
        assert edges[0].source == "1"
        assert edges[0].target == "2"