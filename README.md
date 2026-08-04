# Enterprise RAG API

Production-grade Retrieval-Augmented Generation (RAG) backend service architected with FastAPI, AWS Bedrock, and FAISS. Designed to process enterprise documents, execute high-performance semantic search, and deliver context-aware generative answers via structured REST endpoints.

---

## Architectural Overview

The system implements a modular service-oriented architecture separating core RAG pipelines, configuration management, and API routing:
enterprise-rag-api/
│
├── app/
│   ├── init.py
│   ├── config.py         # Application and environment settings (Pydantic / os.getenv)
│   ├── main.py           # FastAPI entry point and router definitions
│   └── services.py       # Core RAG logic, vector store retrieval, and Bedrock client integration
│
├── data/                 # Source enterprise documents (PDFs, reports, CVs)
├── faiss_index/          # Serialized local vector database indices
├── venv/                 # Python virtual environment
├── .env.example          # Environment variables template
├── .gitignore            # Git exclusion rules for secrets and local caches
└── requirements.txt      # Project dependencies


---

## Technology Stack

* **Web Framework:** FastAPI, Uvicorn
* **Generative AI & LLMs:** AWS Bedrock (Claude, Amazon Nova models)
* **Embeddings:** Amazon Titan Embeddings Model
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **Orchestration:** LangChain
* **Configuration:** Pydantic Settings, Python Dotenv

---

## Prerequisites

* Python 3.10 or higher
* Active AWS Account with Bedrock model access enabled (Region: `eu-central-1` or configured region)
* AWS IAM Credentials with appropriate permissions for Bedrock invocation

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Ibrahim-Mammadov/enterprise-rag-api.git](https://github.com/Ibrahim-Mammadov/enterprise-rag-api.git)
cd enterprise-rag-api
2. Create and Activate Virtual Environment
Bash
python -m venv venv
# On Windows (PowerShell):
./venv/Scripts/Activate.ps1
# On macOS / Linux:
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory based on the following template (.env.example):

Code snippet
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=eu-central-1
Running the Application
Start the FastAPI development server using Uvicorn:

Bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
Once running, access the interactive API documentation (Swagger UI) at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
API Usage
Query Endpoint
Send a POST request to query the ingested document knowledge base.

URL: /query

Method: POST

Content-Type: application/json

Request Body Example:
JSON
{
  "question": "What are the main technical skills, programming languages, and tools listed in this CV?"
}
cURL Command:
Bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/query](http://127.0.0.1:8000/query)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What are the main technical skills, programming languages, and tools listed in this CV?"
}'
{
  "answer": "The main technical skills, programming languages, and tools listed in this CV are:\n\n### Technical Skills:\n- **Generative AI & LLMs**: AWS Bedrock, Claude Models, Amazon Titan, RAG Architecture, LangChain, LangGraph, Prompt Engineering, Enterprise Knowledge Bases\n- **Vector DBs & Search**: Amazon OpenSearch, FAISS, Pinecone, Semantic Search, Vector Embeddings\n- **Data Analytics & Tools**: Python (Pandas, NumPy, Matplotlib), SQL, Data Cleaning & Preprocessing, Exploratory Data Analysis (EDA), KPI/SLA Metrics Tracking, Data Validation\n- **Cloud & DevOps**: AWS (Lambda, API Gateway, S3, CloudWatch, SNS, ECS/EKS), REST APIs (FastAPI), Terraform (IaC), Git, Docker, CI/CD Pipelines\n\n### Programming Languages:\n- **Python**: With libraries such as Pandas, NumPy, and Matplotlib.\n- **SQL**\n\n### Tools:\n- **AWS Services**: Lambda, API Gateway, S3, CloudWatch, SNS, ECS/EKS\n- **Version Control**: Git\n- **Containerization**: Docker\n- **CI/CD**: Continuous Integration/Continuous Deployment Pipelines\n- **Vector Databases & Search**: Amazon OpenSearch, FAISS, Pinecone\n- **Cloud Infrastructure as Code**: Terraform\n\nThese skills and tools reflect a strong background in data analytics, cloud computing, and AI/ML technologies.",
  "sources": [
    "Ibrahim Mammadov AI Engineer.pdf"
  ]
}.
