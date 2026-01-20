import os
from pathlib import Path
from typing import Dict, List

from langchain_core.documents import Document
from langchain_chroma import Chroma
from utils.embeddings import get_embeddings

# Always resolve absolute path
DATA_DIR = Path(__file__).parent.parent / "data"

VECTORSTORE_DIR = Path(__file__).parent.parent / "vectorstore"

def parse_markdown(file_path: Path) -> Document:
    """Parse a markdown file to extract metadata and content."""

    metadata : Dict[str, str] = {}
    content_lines : List[str] = []

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if ":" in line and line.split(":")[0].isupper():
                key, value = line.split(":", 1)
                if key in ["TYPE", "TITLE"]:
                    metadata[key.strip().lower] = value.strip()
                else:
                    content_lines.append(line)
            else:
                content_lines.append(line)

    content = "".join(content_lines).strip()
    # print(metadata)
    # print()
    
    return Document(page_content=content,
                    metadata={
                        "type": metadata.get("type", "unknown"),
                        "title": metadata.get("title", file_path.stem),
                        "source":  str(file_path)
                    })

def load_documents() -> List[Document]:
    """Load and parse all markdown documents from the data directory."""

    documents : List[Document] = []
    
    for file_path in DATA_DIR.rglob("*.md"):
        document = parse_markdown(file_path)
        print(f"Parsed document: {document.metadata['title']} from {file_path}")
        documents.append(document)
    
    return documents

def main():
    """Main function to load documents, create embeddings, and store them in Chroma vector store."""

    # Load documents
    documents = load_documents()
    print(f"Loaded {len(documents)} documents from {DATA_DIR}")
    
    # Initialize embeddings
    embeddings = get_embeddings()
    
    # Create Chroma vector store
    vectorstore = Chroma(collection_name = "portfolio", embedding_function = embeddings, persist_directory=str(VECTORSTORE_DIR))
    
    # Persist the vector store to disk
    vectorstore.add_documents(documents)
    print(f"Vector store persisted at {VECTORSTORE_DIR}")

if __name__ == "__main__":
    main()