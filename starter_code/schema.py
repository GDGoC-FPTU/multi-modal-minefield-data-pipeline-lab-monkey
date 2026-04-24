from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    # TODO: Define the v1 schema. 
    # Suggested fields: document_id, content, source_type, author, timestamp, metadata
    model_config = ConfigDict(extra='allow')
    
    document_id: str
    title: Optional[str] = "Untitled"
    content: str
    source_type: str # e.g., 'PDF', 'Video', 'HTML', 'CSV', 'Code'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None
    
    # You might want a dict for source-specific metadata
    source_metadata: dict[str, Any] = Field(default_factory=dict)
    
    schema_version: str = "v1"
