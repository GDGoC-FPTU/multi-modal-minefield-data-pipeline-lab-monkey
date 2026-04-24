import ast
import re
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # Use the 'ast' module to find docstrings for functions
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {}
        
    docstrings = []
    
    # Get module docstring
    module_doc = ast.get_docstring(tree)
    if module_doc:
        docstrings.append(f"Module Docstring:\n{module_doc}")
        
    # Get function docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                docstrings.append(f"{node.name} Docstring:\n{doc}")
                
    # Use regex to find business rules in comments like "# Business Logic Rule 001"
    # Or just find any comments
    rules = re.findall(r'#.*?(Business Logic Rule.*?)(?=\n|$)', source_code, re.IGNORECASE)
    if not rules:
        # Fallback to any comment with 'business logic'
        rules = re.findall(r'#.*?(business logic.*?)(?=\n|$)', source_code, re.IGNORECASE)
        
    if rules:
        docstrings.append("Inline Rules:\n" + "\n".join(rules))
        
    content = "\n\n".join(docstrings)
    
    doc = {
        "document_id": f"code-legacy-{os.path.basename(file_path)}",
        "content": content,
        "source_type": "Code",
        "author": "Legacy Developer",
        "timestamp": None,
        "source_metadata": {
            "original_file": os.path.basename(file_path)
        }
    }
    
    return doc
