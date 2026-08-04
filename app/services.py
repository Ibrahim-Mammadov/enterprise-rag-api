import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings, ChatBedrock

from app.config import settings

def get_embeddings():
    """Returns Amazon Titan Embeddings model."""
    return BedrockEmbeddings(
        model_id=settings.embedding_model_id,
        region_name=settings.aws_region
    )

def get_llm():
    """Returns Amazon Nova Chat model."""
    return ChatBedrock(
        model_id=settings.llm_model_id,
        region_name=settings.aws_region,
        model_kwargs={"temperature": 0.1}
    )

def process_and_save_document(file_path: str, original_filename: str) -> str:
    """Reads uploaded document, splits into chunks, and indexes into FAISS."""
    file_extension = Path(original_filename).suffix.lower()
    
    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError("Only .pdf and .txt files are supported!")
    
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    embeddings = get_embeddings()
    faiss_dir = Path(settings.faiss_index_path)
    
    if faiss_dir.exists() and any(faiss_dir.iterdir()):
        vector_store = FAISS.load_local(
            settings.faiss_index_path, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
    
    vector_store.save_local(settings.faiss_index_path)
    return f"'{original_filename}' successfully processed and added to vector store."

def ask_rag_system(question: str) -> dict:
    """Retrieves relevant context from FAISS and generates answer using Bedrock LLM."""
    faiss_dir = Path(settings.faiss_index_path)
    
    if not faiss_dir.exists() or not any(faiss_dir.iterdir()):
        return {
            "answer": "No documents uploaded yet. Please upload a document first.",
            "sources": []
        }
    
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        settings.faiss_index_path, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([os.path.basename(doc.metadata.get("source", "Unknown")) for doc in docs]))
    
    llm = get_llm()
    prompt = f"""You are a professional assistant. Answer the user's question honestly and detailed based on the context information below.
If the answer is not in the context, say "The answer to this question is not available in the provided documents."

Context:
{context}

Question: {question}
Answer:"""

    response = llm.invoke(prompt)
    answer_text = response.content if hasattr(response, "content") else str(response)
    
    return {
        "answer": answer_text,
        "sources": sources
    }