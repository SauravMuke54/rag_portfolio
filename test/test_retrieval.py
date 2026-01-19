from langchain_chroma import Chroma
from utils.embeddings import get_embeddings
from pathlib import Path

VECTORSTORE_DIR = Path(__file__).parent.parent / "vectorstore"

vectorstore = Chroma(collection_name = "portfolio", embedding_function = get_embeddings(), persist_directory=VECTORSTORE_DIR)
print("Chroma vector store initialized with collection 'portfolio'.")

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

query = "Which project reduced processing time?"

docs = retriever.invoke(query)
print(f"Retrieved {len(docs)} documents for the query: '{query}'")

for i, doc in enumerate(docs):
    print(f"\nDocument {i+1}:\nTitle: {doc.metadata.get('title', 'N/A')}\nContent: {doc.page_content[:500]}...\n")
