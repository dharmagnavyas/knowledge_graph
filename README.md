A powerful tool that generates knowledge graphs from PDF documents using GraphRAG-SDK and Unstructured-IO, with storage in FalkorDB.
## 🚀 Features
- Automated PDF processing with Unstructured-IO
- Knowledge graph generation using GraphRAG-SDK
- Embedding generation with sentence-transformers
- Efficient graph storage in FalkorDB
- Docker containerization for easy deployment
- Comprehensive error handling and logging
## 📋 Prerequisites
- Docker and Docker Compose
- Python 3.9 or higher
- Git
## 🛠️ Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/knowledge-graph-generator.git
cd knowledge-graph-generator
```
2. Build and start the Docker containers:
```bash
docker-compose up -d
```
## 📁 Project Structure
```
knowledge_graph_generator/
│
├── src/                     # Source code
│   ├── pdf_processor.py     # PDF processing logic
│   ├── graph_generator.py   # Knowledge graph generation
│   ├── database.py         # FalkorDB interactions
│   └── config.py           # Configuration settings
│
├── tests/                  # Test files
├── docker/                 # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```
## 🎯 Usage
1. Place your PDF files in the `data/pdfs` directory
2. The system will automatically:
   - Process new PDFs
   - Generate embeddings
   - Create knowledge graph connections
   - Store results in FalkorDB
3. Monitor the processing:
```bash
docker-compose logs -f
```
## 📚 Recommended PDF Types
For optimal results, use PDFs that contain structured textual information:
- Academic/Research Papers
- Technical Documentation
- Educational Materials
- Business/Industry Reports
PDF Guidelines:
- Text-based (not scanned)
- Clear sections and structure
- 5-20 pages each
- English language content
- Related themes or topics
## 🧪 Testing
Run the test suite:
```bash
docker-compose run knowledge_graph_generator pytest
```
## 🔧 Configuration
Adjust settings in `src/config.py`:
- PDF input directory
- FalkorDB connection details
- Batch processing size
- Embedding model selection
- Chunk size and overlap
## 🚫 Error Handling
The system includes comprehensive error handling for:
- PDF processing issues
- Database connection failures
- Graph generation errors
- Invalid file formats
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
