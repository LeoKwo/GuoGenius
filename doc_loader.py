import PyPDF2

def pdf_to_str(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def txt_to_str(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return text