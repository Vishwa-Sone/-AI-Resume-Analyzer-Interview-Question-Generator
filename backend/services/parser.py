
import fitz        
import docx        
import io         


def parse_resume(file_bytes: bytes, filename: str) -> str:
    
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        return _parse_pdf(file_bytes)
    elif ext == "docx":
        return _parse_docx(file_bytes)
    else:
        raise ValueError(
            f"Unsupported file type: .{ext}. "
            f"Only PDF and DOCX are supported."
        )


def _parse_pdf(file_bytes: bytes) -> str:
    
    text = "" 
    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        text += page.get_text()   
        text += "\n"              

    pdf.close()

    return text.strip()           


def _parse_docx(file_bytes: bytes) -> str:
  
    text = ""
    doc = docx.Document(io.BytesIO(file_bytes))

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():             
            text += paragraph.text + "\n"

    return text.strip()