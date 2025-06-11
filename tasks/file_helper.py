# --- FILE: tasks/file_helper.py ---

import os
import PyPDF2
import docx
from .gemini_helper import ask_gemini

def _summarize_text_with_ai(text, file_path):
    """Internal function to send extracted text to Gemini for summarization."""
    if not text or not text.strip():
        return f"Could not extract any readable text from the file at {file_path}."
    
    print(f"INFO: Sending extracted text from '{os.path.basename(file_path)}' to AI for summarization...")
    
    prompt = f"""
    Please provide a concise, high-level summary of the following document content. 
    Focus on the main points, key findings, and any conclusions.

    DOCUMENT CONTENT:
    ---
    {text[:8000]} 
    ---

    SUMMARY:
    """
    # We slice the text [:8000] to avoid exceeding the token limit for the prompt.
    
    summary = ask_gemini(prompt)
    return f"Here is a summary of '{os.path.basename(file_path)}':\n\n{summary}"

def _extract_text_from_pdf(file_path):
    """Extracts all text from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def _extract_text_from_docx(file_path):
    """Extracts all text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"❌ Error reading DOCX: {e}")
        return ""

def summarize_file(file_path):
    """
    Main function to summarize a file. It determines the file type and calls the appropriate handler.
    """
    clean_path = file_path.strip().strip('"\'') # Clean up potential quotes from the path
    
    if not os.path.exists(clean_path):
        return f"File not found. I could not locate the file at: {clean_path}"

    try:
        _, ext = os.path.splitext(clean_path)
        text_content = ""
        
        if ext.lower() == '.pdf':
            text_content = _extract_text_from_pdf(clean_path)
        elif ext.lower() == '.docx':
            text_content = _extract_text_from_docx(clean_path)
        elif ext.lower() == '.txt':
             with open(clean_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        else:
            return f"Sorry, I can only summarize .pdf, .docx, and .txt files, not the '{ext}' format."
            
        return _summarize_text_with_ai(text_content, clean_path)

    except Exception as e:
        return f"An unexpected error occurred while processing the file: {e}"