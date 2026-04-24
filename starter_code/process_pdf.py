import google.generativeai as genai
import os
import json
import time
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
        
    # Thay đổi model name để tránh lỗi 404 trên các phiên bản API cũ
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print(f"Uploading {file_path} to Gemini...")
    try:
        pdf_file = genai.upload_file(path=file_path)
    except Exception as e:
        print(f"Failed to upload file to Gemini: {e}")
        return None
        
    prompt = """
Analyze this document and extract the following structured metadata: Title, Author, Main Topics, and Tables.
Output exactly as a JSON object matching this exact format:
{
    "document_id": "pdf-doc-001",
    "content": "Main Topics: [Insert Main Topics] \\n Tables: [Insert Tables summary]",
    "source_type": "PDF",
    "author": "[Insert author name here]",
    "timestamp": null,
    "source_metadata": {
        "original_file": "lecture_notes.pdf",
        "title": "[Insert Title here]"
    }
}
"""
    
    print("Generating content from PDF using Gemini...")
    max_retries = 5
    base_delay = 2
    response = None
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content([pdf_file, prompt])
            break
        except ResourceExhausted as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Rate limited (429). Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries exceeded. Failed to generate content.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            
    if not response:
        return None
        
    content_text = response.text
    
    # Simple cleanup if the response is wrapped in markdown json block
    if content_text.startswith("```json"):
        content_text = content_text[7:]
    if content_text.endswith("```"):
        content_text = content_text[:-3]
    if content_text.startswith("```"):
        content_text = content_text[3:]
        
    try:
        extracted_data = json.loads(content_text.strip())
        return extracted_data
    except json.JSONDecodeError:
        print("Failed to decode JSON from Gemini response.")
        return None
