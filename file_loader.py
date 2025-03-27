import os
import pandas as pd
import docx
import PyPDF2

def load_all_documents(directory="sources"):
    texts = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        texts.append(load_text_from_file(path))
    return "\n\n".join(texts)

def load_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        return extract_pdf(file_path)
    elif ext == '.docx':
        return extract_docx(file_path)
    elif ext in ['.csv', '.xlsx']:
        return extract_table(file_path)
    else:
        return f"Format non supporté: {ext}"

def extract_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_table(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df.to_string(index=False)
    except Exception as e:
        return f"Erreur lecture table : {e}"