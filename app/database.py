import uuid
from typing import Any, List, Optional, Tuple

MOCK_CLIENTS = {
    "C-01": {"company": "Northwind Utilities", "purchased_reports": ["R-101", "R-103", "R-102"]},
    "C-02": {"company": "Blue Delta Infra", "purchased_reports": ["R-103", "R-102"]}
}

MOCK_REPORTS = [
    {"sector": "Utilities", "report_count": 3},
    {"sector": "Consumer Durables", "report_count": 1},
    {"sector": "Manufacturing", "report_count": 1},
    {"sector": "Energy", "report_count": 1}
]

def fetch_client_entitlements(client_id: str) -> Tuple[Optional[str], List[str]]:
    if client_id in MOCK_CLIENTS:
        return MOCK_CLIENTS[client_id]["company"], MOCK_CLIENTS[client_id]["purchased_reports"]
    return None, []

def execute_safe_readonly_sql(sql_query: str) -> Tuple[bool, Any]:
    norm = sql_query.lower()
    if any(w in norm for w in ["delete", "drop", "update", "insert", "alter"]):
        return False, "Modifying operations blocked by read-only policy."
    return True, MOCK_REPORTS

def create_escalation_ticket(client_id: str, query: str, reason: str) -> str:
    return f"TICK-{uuid.uuid4().hex[:8].upper()}"
