import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "eu-central-1")
    
    # Model configurations
    embedding_model_id: str = "amazon.titan-embed-text-v1"
    llm_model_id: str = "eu.amazon.nova-lite-v1:0"
    
    # Vector database and data paths
    faiss_index_path: str = "faiss_index"
    data_path: str = "data"

settings = Settings()