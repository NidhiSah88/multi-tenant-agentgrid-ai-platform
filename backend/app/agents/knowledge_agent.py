# specialist agents

def knowledge_agent_node(state: dict) -> dict:
    message = state["user_message"]

    return {
        "agent_response": (
            f"You asked: {message}. "
            "I can help you with property details, pricing, "
            "locations and amenities."
        ),
        "intent": "property_information",
    }




