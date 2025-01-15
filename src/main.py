import logging
from pathlib import Path
from config import config
from pdf_processor import PDFProcessor
from graph_generator import KnowledgeGraphGenerator
from database import FalkorDBClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        logger.info("Initializing components...")
        pdf_processor = PDFProcessor(config.pdf_input_dir)
        graph_generator = KnowledgeGraphGenerator(
            config.embedding_model,
            config.chunk_size,
            config.chunk_overlap
        )
        db_client = FalkorDBClient(config.falkordb_host, config.falkordb_port)

        # Get list of processed files
        processed_files = db_client.get_processed_files()
        logger.info(f"Found {len(processed_files)} previously processed files")

        # Get new PDFs to process
        new_pdfs = pdf_processor.get_new_pdfs(processed_files)
        logger.info(f"Found {len(new_pdfs)} new PDFs to process")

        # Process PDFs in batches
        for pdf_path in new_pdfs:
            logger.info(f"Processing PDF: {pdf_path}")
            
            try:
                # Extract content from PDF
                elements = pdf_processor.process_pdf(pdf_path)
                
                # Generate nodes and edges
                nodes = graph_generator.create_nodes(elements)
                edges = graph_generator.create_edges(nodes)
                
                # Update graph
                graph_generator.update_graph(nodes, edges)
                
                # Store in database
                for node in nodes:
                    node_data = {
                        "content": node.content,
                        "filename": pdf_path.name,
                        "embedding": node.embedding.tolist(),
                        **node.metadata
                    }
                    db_client.store_node(node.id, node_data)
                
                for edge in edges:
                    db_client.store_edge(
                        edge.source,
                        edge.target,
                        {"weight": edge.weight}
                    )
                
                logger.info(f"Successfully processed and stored {pdf_path}")
                
            except Exception as e:
                logger.error(f"Error processing {pdf_path}: {str(e)}")
                continue

        logger.info("Knowledge graph generation completed successfully")

    except Exception as e:
        logger.error(f"Error during knowledge graph generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()