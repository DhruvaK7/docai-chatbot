import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
INDEX_PATH = "./embeddings/faiss_index"
