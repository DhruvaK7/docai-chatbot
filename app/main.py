# main.py
from fastapi import FastAPI, UploadFile, Form
import openai
import fitz  # PyMuPDF
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = FastAPI()

# Dummy vector store
class VectorStore:
    def __init__(self):
        self.vectors = []
        self.texts = []

    def add(self, vectors, texts):
        self.vectors.extend(vectors)
        self.texts.extend(texts)

    def search(self, q_vec):
        return self.texts[:3]  # Return top 3 matches (mock)

VECTOR_STORE = VectorStore()

# Config values
OPENAI_API_KEY = "sk-..."  # Use your real/test key
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

openai.api_key = OPENAI_API_KEY

# Core functions
def get_embedding(text, model="text-embedding-3-small"):
    response = openai.Embedding.create(input=[text], model=model)
    return response["data"][0]["embedding"]

def process_document(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_text(text)
    vectors = [get_embedding(c) for c in chunks]
    VECTOR_STORE.add(vectors, chunks)

def answer_question(question):
    q_vec = get_embedding(question)
    context = "\n\n".join(VECTOR_STORE.search(q_vec))
    prompt = f"""You are an AI assistant. Use only the context below to answer.

Context:
{context}

Question:
{question}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

async def parse_file(file: UploadFile):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=content, filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.filename.endswith(".docx"):
        document = docx.Document(file.file)
        return "\n".join([para.text for para in document.paragraphs])
    else:
        return content.decode("utf-8")

# Routes
@app.post("/upload")
async def upload(file: UploadFile):
    text = await parse_file(file)
    process_document(text)
    return {"status": "Processed"}

@app.post("/query")
async def ask_question(question: str = Form(...)):
    return {"answer": answer_question(question)}
