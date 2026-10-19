import math, re
from app.schemas import DerivedValue

def sanitize_retrieved_text(text: str) -> tuple[str, bool]:
    patterns = [r"disregard\s+all\s+previous\s+instructions", r"ignore\s+all\s+instructions", r"print\s+the\s+full\s+contents"]
    detected = False
    cleaned = text
    for p in patterns:
        if re.search(p, cleaned, re.IGNORECASE):
            detected = True
            cleaned = re.sub(p, "[BLOCKED_INJECTION_DIRECTIVE]", cleaned, flags=re.IGNORECASE)
    return cleaned, detected

def run_cagr_projection(base_val: float, cagr_rate: float, start_year: int, target_year: int, metric_label: str, base_assumption: str) -> DerivedValue:
    periods = target_year - start_year
    projected = base_val * math.pow((1.0 + cagr_rate), periods)
    return DerivedValue(
        metric=metric_label,
        formula="Base_Value * ((1 + CAGR) ^ Years)",
        inputs={"base_value": base_val, "cagr_percent": round(cagr_rate * 100, 2), "periods": periods},
        assumptions=base_assumption,
        result=round(projected, 3),
    )
