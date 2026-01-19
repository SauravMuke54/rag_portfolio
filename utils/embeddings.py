from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    """
    Initialize and return a HuggingFaceEmbeddings instance.

    Args:
        model_name (str): The name of the Hugging Face model to use for embeddings.

    Returns:
        HuggingFaceEmbeddings: An instance of HuggingFaceEmbeddings.
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings
