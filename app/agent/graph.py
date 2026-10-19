from langgraph.graph import END, StateGraph
from app.agent.state import ReportCopilotState
from app.agent.nodes import (
    guardrail_node, router_node, retriever_node, sql_executor_node,
    calculator_node, writer_node, critic_node, escalation_node
)

def route_decision(state: ReportCopilotState) -> str:
    intent = state.get("intent")
    if intent in ["injection_refusal", "out_of_scope"]: return "writer"
    if intent == "sql_aggregate": return "sql_executor"
    return "retriever"

def critic_decision(state: ReportCopilotState) -> str:
    return "escalation" if state.get("escalated") else END

def build_atlas_graph():
    wf = StateGraph(ReportCopilotState)
    wf.add_node("guardrail", guardrail_node)
    wf.add_node("router", router_node)
    wf.add_node("retriever", retriever_node)
    wf.add_node("sql_executor", sql_executor_node)
    wf.add_node("calculator", calculator_node)
    wf.add_node("writer", writer_node)
    wf.add_node("critic", critic_node)
    wf.add_node("escalation", escalation_node)

    wf.set_entry_point("guardrail")
    wf.add_edge("guardrail", "router")
    wf.add_conditional_edges("router", route_decision, {"writer": "writer", "sql_executor": "sql_executor", "retriever": "retriever"})
    wf.add_edge("sql_executor", "writer")
    wf.add_edge("retriever", "calculator")
    wf.add_edge("calculator", "writer")
    wf.add_edge("writer", "critic")
    wf.add_conditional_edges("critic", critic_decision, {"escalation": "escalation", END: END})
    wf.add_edge("escalation", END)
    return wf.compile()

atlas_agent = build_atlas_graph()
