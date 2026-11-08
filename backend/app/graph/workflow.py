from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState

from app.agents.supervisor import supervisor_node
from app.agents.knowledge_agent import knowledge_agent_node
from app.agents.lead_agent import lead_agent_node
from app.agents.workflow_agent import workflow_agent_node


def route_agent(state: AgentState):
    return state["selected_agent"]


def route_after_lead(state: AgentState):
    if state.get("next_step") == "workflow":
        return "workflow"

    # Return the label "end", not the END constant.
    return "end"


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("knowledge", knowledge_agent_node)
    graph.add_node("lead", lead_agent_node)
    graph.add_node("workflow", workflow_agent_node)

    graph.add_edge(START, "supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_agent,
        {
            "knowledge": "knowledge",
            "lead": "lead",
        },
    )

    graph.add_edge("knowledge", END)

    graph.add_conditional_edges(
        "lead",
        route_after_lead,
        {
            "workflow": "workflow",
            "end": END,
        },
    )

    graph.add_edge("workflow", END)

    return graph.compile()


agent_graph = build_agent_graph()




