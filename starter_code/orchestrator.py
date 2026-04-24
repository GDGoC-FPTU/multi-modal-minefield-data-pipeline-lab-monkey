import json
import time
import os

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    
    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")
    trans_path = os.path.join(RAW_DATA_DIR, "demo_transcript.txt")
    html_path = os.path.join(RAW_DATA_DIR, "product_catalog.html")
    csv_path = os.path.join(RAW_DATA_DIR, "sales_records.csv")
    code_path = os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    # ----------------------------------------------

    # Gather all raw documents
    docs_to_process = []
    
    pdf_doc = extract_pdf_data(pdf_path)
    if pdf_doc: docs_to_process.append(pdf_doc)
        
    trans_doc = clean_transcript(trans_path)
    if trans_doc: docs_to_process.append(trans_doc)
        
    docs_to_process.extend(parse_html_catalog(html_path))
    docs_to_process.extend(process_sales_csv(csv_path))
    
    code_doc = extract_logic_from_code(code_path)
    if code_doc: docs_to_process.append(code_doc)
        
    # Process through QA gates and Schema validation
    for raw_doc in docs_to_process:
        if run_quality_gate(raw_doc):
            try:
                # Validate against the Unified Schema
                unified_doc = UnifiedDocument(**raw_doc)
                # Append a JSON-safe dictionary (handles datetime automatically)
                final_kb.append(unified_doc.model_dump(mode='json'))
            except Exception as e:
                print(f"Validation Error for {raw_doc.get('document_id', 'unknown')}: {e}")
                
    # Save the final Knowledge Base
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_kb, f, ensure_ascii=False, indent=2)

    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.2f} seconds.")
    print(f"Total valid documents stored: {len(final_kb)}")


if __name__ == "__main__":
    main()
