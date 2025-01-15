from pathlib import Path
from typing import List, Dict
import PyPDF2
import uuid
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF processing using PyPDF2"""
    
    def __init__(self, input_dir: str):
        self.input_dir = Path(input_dir)
        
    def process_pdf(self, pdf_path: Path) -> List[Dict]:
        """Process a single PDF file and return structured elements"""
        try:
            elements = []
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():  # Only add non-empty pages
                        elements.append({
                            "element_id": str(uuid.uuid4()),
                            "text": text,
                            "type": "paragraph",
                            "page_number": page_num,
                            "filename": pdf_path.name
                        })
            return elements
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
            
    def get_new_pdfs(self, processed_files: List[str]) -> List[Path]:
        """Get list of PDFs that haven't been processed yet"""
        all_pdfs = list(self.input_dir.glob("*.pdf"))
        return [pdf for pdf in all_pdfs if pdf.name not in processed_files]