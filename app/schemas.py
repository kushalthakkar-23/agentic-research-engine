from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Citation(BaseModel):
    report_id: str
    title: str
    page: int
    quoted_text: str

class DerivedValue(BaseModel):
    metric: str
    formula: str
    inputs: Dict[str, Any]
    assumptions: str
    result: float

class ChatRequest(BaseModel):
    client_id: str
    query: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    confidence: float
    conflicts: List[str] = Field(default_factory=list)
    derived_values: List[DerivedValue] = Field(default_factory=list)
    escalated: bool = False
    ticket_id: Optional[str] = None
    injection_detected: bool = False
