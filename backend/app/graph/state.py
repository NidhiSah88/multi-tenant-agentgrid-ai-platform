from typing import TypedDict, Optional


class AgentState(TypedDict):
    tenant_id: str
    conversation_id: str
    user_message: str

    customer_name: Optional[str]
    contact_number: Optional[str]

    intent: Optional[str]
    selected_agent: Optional[str]

    agent_response: Optional[str]
    lead_data: Optional[dict]
    lead_id: Optional[str]

    requires_human_approval: bool
    next_step: Optional[str]




    