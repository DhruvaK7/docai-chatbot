#import fitz
#print("Imported fitz")

#import docx
#print("Imported docx")

#async def parse_file(file):
#    content = await file.read()

#    if file.filename.endswith(".pdf"):
#        doc = fitz.open(stream=content, filetype="pdf")
#        return "\n".join([page.get_text() for page in doc])

#    elif file.filename.endswith(".docx"):
#        document = docx.Document(file.file)
#        return "\n".join([para.text for para in document.paragraphs])

#    else:
#        return content.decode("utf-8")

def test_import():
    print("parse_file is defined:", "parse_file" in globals())

if __name__ == "__main__":
    test_import()