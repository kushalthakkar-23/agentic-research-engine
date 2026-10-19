from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict
from app.schemas import Citation, DerivedValue

class ReportCopilotState(TypedDict):
    client_id: str
    company_name: str
    query: str
    allowed_reports: List[str]
    intent: str
    injection_detected: bool
    refusal_reason: Optional[str]
    retrieved_chunks: List[Dict[str, Any]]
    sql_query: Optional[str]
    sql_results: Optional[List[Dict[str, Any]]]
    derived_values: List[DerivedValue]
    draft_answer: str
    conflicts: List[str]
    citations: List[Citation]
    confidence: float
    escalated: bool
    ticket_id: Optional[str]
