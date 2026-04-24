import re
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # Remove noise tokens like [Music], [inaudible], [Laughter]
    text_clean = re.sub(r'\[[a-zA-Z\s]+\]', '', text)
    
    # Strip timestamps [00:00:00]
    text_clean = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text_clean)
    
    # Clean up extra spaces
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()
    
    # Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    price_match = re.search(r'(năm trăm nghìn)', text, re.IGNORECASE)
    price_vn = price_match.group(1) if price_match else None
    
    doc = {
        "document_id": f"transcript-{os.path.basename(file_path)}",
        "content": text_clean,
        "source_type": "Video",
        "author": "Unknown",
        "timestamp": None,
        "source_metadata": {
            "original_file": os.path.basename(file_path),
            "extracted_price_vn": price_vn
        }
    }
    
    return doc
