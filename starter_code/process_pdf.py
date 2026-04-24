from google import genai
from google.genai.errors import APIError
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
        
    # Initialize the new genai Client. It automatically picks up GEMINI_API_KEY from env.
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")
        return None
    
    print(f"Uploading {file_path} to Gemini...")
    try:
        pdf_file = client.files.upload(file=file_path)
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
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[pdf_file, prompt]
            )
            break
        except APIError as e:
            if getattr(e, 'code', None) == 429: # ResourceExhausted
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limited (429). Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("Max retries exceeded. Failed to generate content.")
                    return None
            else:
                print(f"API Error occurred: {e}")
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
