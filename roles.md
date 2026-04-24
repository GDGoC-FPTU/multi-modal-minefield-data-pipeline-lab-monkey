# Team Roles & Responsibilities

Since the team consists of 3 members instead of the originally planned 4, the roles and responsibilities for **Codelab 03 v1: The Multi-Modal Minefield (Advanced Edition)** have been redistributed as follows. This document outlines exactly what each member needs to do and which files they are responsible for.

## 1. Lâm Hoàng Hải
**Roles**: Lead Data Architect & DevOps & Integration Specialist (Roles 1 & 4 combined)

### Data Architect Responsibilities:
- **Main File**: `starter_code/schema.py`
- **Objective**: Define the `UnifiedDocument` using Pydantic.
- **The Challenge**: Anticipate the mid-lab schema migration. At the 60-minute mark, a breaking change will be announced requiring a schema update to v2 (e.g., field renames). You must be ready to migrate the schema without breaking the pipeline.

### DevOps & Integration Responsibilities:
- **Main File**: `starter_code/orchestrator.py`
- **Objective**: Orchestrate the DAG and ensure the final JSON is valid.
- **Key Tasks**:
  - Connect all processing parts into a single execution flow (DAG).
  - Import and call the processing functions created by the ETL Builder.
  - Save the final result as `processed_knowledge_base.json` in the root directory.
  - Track and measure processing time (SLA tracking).

## 2. Khổng Mạnh Tuấn
**Role**: ETL/ELT Builder (Role 2)

### ETL/ELT Builder Responsibilities:
- **Main Files**: `process_pdf.py`, `process_csv.py`, `process_html.py`, `process_transcript.py`, `process_legacy_code.py` (inside `starter_code/`)
- **Objective**: Extract clean, structured data from messy, multi-source data.
- **Key Tasks**:
  - **PDF Extraction**: Use the Gemini API to extract structured metadata (Title, Author, Main Topics, Tables) from `lecture_notes.pdf`. Implement Exponential Backoff for handling `429` errors.
  - **CSV Processing**: Handle type traps, duplicate IDs, and mixed price/date formats (e.g., "$1200" vs "500000").
  - **Transcript Processing**: Clean up noise tokens (e.g., `[Music]`), speaker labels, and timestamps (e.g., `[00:05:12]`).
  - **HTML Processing**: Differentiate between boilerplate (nav/footer) and actual content (tables).
  - **Legacy Code**: Extract business rules hidden in docstrings using the `ast` module without executing the code.

## 3. Lương Anh Tuấn
**Role**: Observability & QA Engineer (Role 3)

### Observability & QA Responsibilities:
- **Main File**: `starter_code/quality_check.py`
- **Objective**: Act as the "Watchman" by writing semantic gates and capturing business logic.
- **Key Tasks**:
  - Write semantic validation checks to ensure no garbage data enters the final output.
  - Filter out toxic or erroneous strings (e.g., accidental error messages from extraction).
  - Detect semantic drift (e.g., ensuring logic specified in comments matches the actual values).
  - Prepare the pipeline to successfully pass the automated `agent_forensic.py` debrief at the end of the lab.
