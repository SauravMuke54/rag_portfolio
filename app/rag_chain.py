from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from .prompt import PORTFOLIO_SYSTEM_PROMPT # done for streamlit deployement remove . in other cases
# from langchain_core.memory import ConversationBufferMemory
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from utils.embeddings import get_embeddings
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

VECTORSTORE_DIR = Path(__file__).parent.parent / "vectorstore"

def build_rag_chain():

    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name="portfolio",
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(
        # search_type="similarity",
        search_kwargs={"k": 5}
    )

    llm = ChatGroq(
    model=os.getenv("GROQ_MODEL_NAME", "groq/compound"),
    temperature=0.2
)

    prompt = PromptTemplate(template = PORTFOLIO_SYSTEM_PROMPT,
                            input_variables = ["context", "question"])
 
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,output_key="answer")

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain

