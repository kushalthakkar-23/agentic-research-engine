# Project Atlas: Market Intelligence Report Copilot

Project Atlas is an enterprise-grade AI copilot designed to parse, analyze, and synthesize proprietary market research intelligence. The system enforces tenant-level access entitlements, blocks adversarial prompt injections, deterministically handles conflicting market report scopes, executes compound annual growth rate (CAGR) projections, and triggers analyst escalation tickets when queries exceed verified forecast horizons.

---

## 1. System Architecture

The agent executes as a stateful directed graph (ReportCopilotState) using LangGraph. Each node acts as an isolated checkpoint to ensure safety, accurate retrieval, and deterministic computation before drafting responses:

- Inbound Client Request -> guardrail_node (checks prompt injection)
- If injection detected -> Immediate Policy Refusal
- If clean -> router_node (determines sql_aggregate vs rag_research)
- If SQL -> sql_executor_node -> writer_node
- If RAG -> retriever_node (with entitlement pre-filtering) -> calculator_node (deterministic CAGR) -> writer_node
- writer_node -> critic_node (checks confidence score and forecast horizon)
- If confidence < 0.70 or horizon > 2030 -> escalation_node (logs analyst ticket to SQLite)
- Otherwise -> Return verified response with citations

---

## 2. Setup & Execution Instructions

### Prerequisites
- Python 3.10 or higher
- Virtual environment (venv)
- Package Manager: pip

### Installation & Run Steps

1. Activate virtual environment:
   .\.venv\Scripts\Activate.ps1

2. Install dependencies:
   pip install -r requirements.txt

3. Start API server:
   uvicorn main:app --reload

4. Interactive Documentation:
   - Swagger UI: http://127.0.0.1:8000/docs
   - Health Check: http://127.0.0.1:8000/health

---

## 3. Design Decisions & Trade-Offs

- Orchestration (LangGraph State Machine vs ReAct Loop): ReAct architectures can enter non-deterministic loops. A state machine provides strict execution checkpoints and auditing guarantees.
- Entitlements (Pre-retrieval Filtering vs Post-generation Redaction): Post-generation redaction wastes LLM tokens and risks data leakage. Filtering allowed report IDs directly at the vector layer guarantees strict multi-tenant isolation.
- Conflict Resolution (Explicit Scope Reconciliation vs LLM Synthesis): Models tend to blend diverging statistics across distinct scopes (e.g., hardware-only vs total market). Hard boundaries prevent misleading arithmetic synthesis.
- Market Calculations (Deterministic Python Tools vs LLM Arithmetic): Models suffer from compounding precision drift over multi-year horizons. Dedicated pure-function tools ensure reproducible values.

---

## 4. Key Deliverables & Documentation

- Evaluation Report & Failure Analysis: [EVALUATION.md](EVALUATION.md)
- Engineering Roadmap: [WHAT_I_WOULD_DO_WITH_ONE_MORE_WEEK.md](WHAT_I_WOULD_DO_WITH_ONE_MORE_WEEK.md)
- Demo Video Walkthrough: [Watch the 3-5 Minute Demo Video](PASTE_YOUR_LINK_HERE)
