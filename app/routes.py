from fastapi import APIRouter, UploadFile, Form
from .chatbot import answer_question, process_document

import fitz  # PyMuPDF
import docx

router = APIRouter()

async def parse_file(file: UploadFile) -> str:
    content = await file.read()
    
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=content, filetype="pdf")
        return "\n".join([page.get_text() for page in doc])

    elif file.filename.endswith(".docx"):
        document = docx.Document(file.file)
        return "\n".join([para.text for para in document.paragraphs])

    else:
        return content.decode("utf-8")

@router.post("/upload")
async def upload(file: UploadFile):
    text = await parse_file(file)
    process_document(text, file.filename)
    return {"status": "Processed"}

@router.post("/query")
async def ask_question(question: str = Form(...)):
    return {"answer": answer_question(question)}
