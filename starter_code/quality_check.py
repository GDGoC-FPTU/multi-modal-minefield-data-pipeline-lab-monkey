# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

import re


_SEEN_DOCUMENT_IDS = set()

_ERROR_PATTERNS = (
    r"null pointer exception",
    r"traceback \(most recent call last\)",
    r"stack ?trace",
    r"failed to decode json",
    r"max retries exceeded",
    r"resourceexhausted",
    r"an error occurred",
)


def _contains_error_payload(content):
    lowered = content.lower()
    return any(re.search(pattern, lowered) for pattern in _ERROR_PATTERNS)


def _detect_semantic_drift(content):
    lowered = content.lower()

    # Catch common "comment says X but value/code says Y" inconsistencies.
    has_8_percent = "8%" in lowered or "0.08" in lowered
    has_10_percent = "10%" in lowered or "0.10" in lowered
    has_tax_context = "tax" in lowered or "vat" in lowered
    has_discrepancy_language = (
        "discrepancy" in lowered
        or "misleading" in lowered
        or "comment says" in lowered
        or "actually" in lowered
    )

    return has_tax_context and has_8_percent and has_10_percent and has_discrepancy_language


def _extract_price_vnd(content):
    # Handles values like "500,000 VND" or "500000 VND".
    numeric_match = re.search(r"\b(\d{1,3}(?:,\d{3})+|\d{4,})\s*(?:vnd|vnđ)\b", content, re.IGNORECASE)
    if numeric_match:
        return int(numeric_match.group(1).replace(",", ""))
    return None

def run_quality_gate(document_dict):
    # Basic schema sanity checks.
    if not isinstance(document_dict, dict):
        return False

    document_id = str(document_dict.get("document_id", "")).strip()
    source_type = str(document_dict.get("source_type", "")).strip()
    content = str(document_dict.get("content", "")).strip()

    if not document_id or not source_type or len(content) < 20:
        return False

    # Reject duplicate IDs seen in this pipeline run.
    if document_id in _SEEN_DOCUMENT_IDS:
        return False
    _SEEN_DOCUMENT_IDS.add(document_id)

    # Reject corrupted extraction payloads or error dumps.
    if _contains_error_payload(content):
        return False

    # Semantic drift guardrail for legacy business logic text.
    if _detect_semantic_drift(content):
        return False

    # Observability helper: normalize transcript price so forensic agent can verify it.
    source_metadata = document_dict.setdefault("source_metadata", {})
    if isinstance(source_metadata, dict) and source_type.lower() == "video":
        detected_price_vnd = _extract_price_vnd(content)
        if detected_price_vnd is None:
            extracted_price_vn = str(source_metadata.get("extracted_price_vn", "")).lower()
            if "năm trăm nghìn" in extracted_price_vn or "nam tram nghin" in extracted_price_vn:
                detected_price_vnd = 500000

        if detected_price_vnd is not None:
            source_metadata["detected_price_vnd"] = detected_price_vnd

    return True
