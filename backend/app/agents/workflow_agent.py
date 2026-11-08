

from app.services.lead_service import create_lead


def workflow_agent_node(state: dict) -> dict:

    lead_data = state.get("lead_data")

    if not lead_data or lead_data.get("status") != "ready_for_approval":
        return {
            "requires_human_approval": False,
        }

    lead = create_lead(
        tenant_id=state["tenant_id"],
        customer_name=lead_data["customer_name"],
        contact_number=lead_data["contact_number"],
    )

    return {
        "lead_id": lead["lead_id"],
        "lead_data": lead,
        "agent_response": (
            "Your appointment request has been submitted. "
            "Our team will review it and contact you."
        ),
        "requires_human_approval": True,
        "next_step": "human_approval",
    }








