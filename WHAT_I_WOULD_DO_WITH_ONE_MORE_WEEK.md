# What I Would Do With One More Week
**Project Atlas Enhancement Roadmap**  
**Author:** Kushal  
**Focus:** Production Hardening, Dynamic Orchestration, and Evaluation Observability  

---

If granted an additional week to iterate on Project Atlas, I would transition the system from a working prototype into an enterprise-ready, production-grade intelligence copilot across the following four technical initiatives:

### 1. Hybrid Search Architecture & Vector Database Migration
The current prototype uses an in-memory FAISS vector index with mock pre-filtering. While fast, it cannot scale to thousands of concurrent enterprise tenants.
- **Migration**: Migrate from local FAISS to a managed instance of **Qdrant** or **PostgreSQL with pgvector**.
- **Hybrid Retrieval**: Combine dense semantic embeddings with sparse BM25 keyword matching via a Reciprocal Rank Fusion (RRF) pipeline.
- **Reranking**: Add a cross-encoder reranker (e.g., `bge-reranker-large` or Cohere Rerank) to improve retrieval precision before feeding chunks into the agent context.

### 2. Autonomous Agentic Supervisors & Dynamic Function Calling
The system currently uses deterministic string heuristics in `router_node`. While this guarantees low latency and predictable routing, it limits flexibility for nuanced natural language queries.
- **LLM Function Calling**: Implement a LangGraph supervisor pattern where an instruction-tuned model dynamically chooses when to call the SQL engine, vector store, or math tools.
- **Multi-Hop Synthesis**: Allow the agent to gather data across multiple iterations (e.g., query SQL to find available reports, then query vectors for each report to build a comparative table).

### 3. Asynchronous Human-in-the-Loop (HITL) Analyst Workflow
Currently, when a query exceeds the 2030 horizon or falls below the 0.70 confidence threshold, `escalation_node` simply writes a placeholder ticket record to the SQLite database.
- **Queue Pipeline**: Decouple escalations into an asynchronous task queue using **Celery** or **Redis Streams**.
- **Ticketing Integration**: Integrate webhooks to automatically generate tickets in Jira Service Desk or Zendesk.
- **WebSocket State Resumption**: Implement WebSockets so an analyst can update or approve a draft response, streaming the verified answer back to the user's active session.

### 4. Automated CI/CD Regression Evaluation Suite
To safeguard against regression and monitor model drift:
- **Synthetic Test Dataset**: Build a continuous benchmarking pipeline with **DeepEval** and **LangSmith** using 100+ evaluation cases covering prompt injections, out-of-scope prompts, and mathematical edge cases.
- **CI Enforcement**: Add GitHub Actions workflows to run end-to-end tests, evaluate retrieval faithfulness, and audit permissions on every pull request.
