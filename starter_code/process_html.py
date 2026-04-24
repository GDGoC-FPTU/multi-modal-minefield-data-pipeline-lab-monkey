from bs4 import BeautifulSoup
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # Use BeautifulSoup to find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
        
    tbody = table.find('tbody')
    if not tbody:
        return []
        
    documents = []
    
    # Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    for tr in tbody.find_all('tr'):
        cols = tr.find_all('td')
        if len(cols) < 6:
            continue
            
        sp_id = cols[0].text.strip()
        name = cols[1].text.strip()
        category = cols[2].text.strip()
        price_text = cols[3].text.strip()
        stock = cols[4].text.strip()
        rating = cols[5].text.strip()
        
        # Clean price
        price_val = None
        if price_text not in ('N/A', 'Liên hệ'):
            try:
                # Remove ' VND', commas, and try to parse
                clean_p = price_text.replace(' VND', '').replace(',', '')
                price_val = float(clean_p)
            except ValueError:
                pass
                
        content = f"Product: {name}, Category: {category}, Price: {price_text}, Stock: {stock}, Rating: {rating}"
        
        doc = {
            "document_id": f"html-catalog-{sp_id}",
            "content": content,
            "source_type": "HTML",
            "author": "VinShop Catalog",
            "timestamp": None,
            "source_metadata": {
                "original_file": os.path.basename(file_path),
                "price_raw": price_text,
                "price": price_val
            }
        }
        documents.append(doc)
        
    return documents
