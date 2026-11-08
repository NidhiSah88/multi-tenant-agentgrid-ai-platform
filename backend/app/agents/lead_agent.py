
def lead_agent_node(state: dict) -> dict:

    customer_name = state.get("customer_name")
    contact_number = state.get("contact_number")

    if not customer_name or not contact_number:
        return {
            "agent_response": (
                "I'd be happy to arrange a property visit. "
                "Could you share your name and contact number?"
            ),
            "intent": "lead_generation",
            "lead_data": {
                "status": "pending_details"
            },
            "requires_human_approval": False,
            "next_step": "collect_details",
        }

    return {
        "agent_response": (
            "Thank you! I've collected your details. "
            "Your appointment request will be submitted "
            "for human approval."
        ),
        "intent": "lead_generation",
        "lead_data": {
            "customer_name": customer_name,
            "contact_number": contact_number,
            "status": "ready_for_approval",
        },
        "requires_human_approval": True,
        "next_step": "workflow",
    }













# def lead_agent_node(state: dict) -> dict:
#     return {
#         "agent_response": (
#             "I'd be happy to help arrange a property visit. "
#             "Could you share your name and contact number?"
#         ),
#         "intent": "lead_generation",
#         "requires_human_approval": True,
#         "lead_data": {
#             "status": "pending_details",
#             "source": "agentgrid_chat",
#         },
#     }






