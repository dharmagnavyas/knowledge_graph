import pytest
from src.database import FalkorDBClient

def test_database_initialization(test_config):
    client = FalkorDBClient(test_config.falkordb_host, test_config.falkordb_port)
    assert client.redis_conn is not None
    assert client.graph is not None

@pytest.mark.integration
def test_store_node(test_config):
    client = FalkorDBClient(test_config.falkordb_host, test_config.falkordb_port)
    node_properties = {
        "content": "Test content",
        "filename": "test.pdf"
    }
    
    client.store_node("test_node", node_properties)
    client.commit()
    
    # Verify node was stored
    processed_files = client.get_processed_files()
    assert "test.pdf" in processed_files

@pytest.mark.integration
def test_store_edge(test_config):
    client = FalkorDBClient(test_config.falkordb_host, test_config.falkordb_port)
    
    # Create test nodes
    client.store_node("source_node", {"content": "Source content"})
    client.store_node("target_node", {"content": "Target content"})
    
    # Create edge
    edge_properties = {"weight": 0.8}
    client.store_edge("source_node", "target_node", edge_properties)
    client.commit()
    
    # Verify edge exists (would need custom query)
    # This is a simplified test - you might want to add more verification

def test_get_processed_files(test_config, mocker):
    client = FalkorDBClient(test_config.falkordb_host, test_config.falkordb_port)
    
    # Mock query result
    mock_result = mocker.Mock()
    mock_result.result_set = [["file1.pdf"], ["file2.pdf"]]
    mocker.patch.object(client.graph, 'query', return_value=mock_result)
    
    processed_files = client.get_processed_files()
    assert len(processed_files) == 2
    assert "file1.pdf" in processed_files
    assert "file2.pdf" in processed_files