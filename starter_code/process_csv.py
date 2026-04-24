import pandas as pd
from datetime import datetime
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    def clean_price(x):
        if pd.isna(x): return None
        x = str(x).lower().replace('$', '').replace(',', '').strip()
        if x == 'five dollars': return 5.0
        if x in ('n/a', 'null', 'liên hệ', 'nan'): return None
        try:
            return float(x)
        except ValueError:
            return None
            
    df['price'] = df['price'].apply(clean_price)
    
    # Normalize 'date_of_sale' into a datetime object
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], format='mixed', errors='coerce')
    
    # Return a list of dictionaries for the UnifiedDocument schema.
    documents = []
    for _, row in df.iterrows():
        # Handle nan values gracefully
        product_name = row.get('product_name', '')
        if pd.isna(product_name): product_name = ''
        category = row.get('category', '')
        if pd.isna(category): category = ''
            
        content = f"Product: {product_name}, Category: {category}, Price: {row.get('price')} {row.get('currency', '')}, Stock: {row.get('stock_quantity', '')}"
        
        # Convert timestamp to native python datetime or None
        dt_val = row.get('date_of_sale')
        timestamp_val = dt_val.to_pydatetime() if pd.notna(dt_val) else None
        
        doc = {
            "document_id": f"csv-sales-{int(row['id']) if pd.notna(row['id']) else 'unknown'}",
            "content": content,
            "source_type": "CSV",
            "author": str(row.get('seller_id', 'Unknown')),
            "timestamp": timestamp_val,
            "source_metadata": {
                "original_file": os.path.basename(file_path),
                "price": row.get('price'),
                "currency": row.get('currency')
            }
        }
        documents.append(doc)
        
    return documents
