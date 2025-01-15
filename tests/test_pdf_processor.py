import pytest
from pathlib import Path
from src.pdf_processor import PDFProcessor

def test_pdf_processor_initialization(test_config):
    processor = PDFProcessor(test_config.pdf_input_dir)
    assert processor.input_dir == Path(test_config.pdf_input_dir)

def test_process_pdf(test_config, mocker):
    processor = PDFProcessor(test_config.pdf_input_dir)
    mock_pdf_path = Path("tests/data/pdfs/test.pdf")
    
    # Mock partition_pdf function
    mock_elements = [{"text": "Test content", "element_id": "1"}]
    mocker.patch('src.pdf_processor.partition_pdf', return_value=mock_elements)
    
    result = processor.process_pdf(mock_pdf_path)
    assert len(result) > 0
    assert "text" in result[0]

def test_get_new_pdfs(test_config, tmp_path):
    # Create temporary test directory with PDF files
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    (pdf_dir / "test1.pdf").touch()
    (pdf_dir / "test2.pdf").touch()
    
    processor = PDFProcessor(str(pdf_dir))
    processed_files = ["test1.pdf"]
    
    new_pdfs = processor.get_new_pdfs(processed_files)
    assert len(new_pdfs) == 1
    assert new_pdfs[0].name == "test2.pdf"

def test_error_handling(test_config):
    processor = PDFProcessor(test_config.pdf_input_dir)
    with pytest.raises(Exception):
        processor.process_pdf(Path("nonexistent.pdf"))