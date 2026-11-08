
from fastapi import APIRouter
from pydantic import BaseModel, Field
from uuid import uuid4

from app.graph.workflow import agent_graph

router = APIRouter()


class ChatRequest(BaseModel):
    tenant_id: str = "demo-tenant"
    conversation_id: str | None = None
    message: str = Field(min_length=1, max_length=4000)

    customer_name: str | None = None
    contact_number: str | None = None


@router.post("/chat")
async def chat(request: ChatRequest):

    initial_state = {
        "tenant_id": request.tenant_id,
        "conversation_id": request.conversation_id or str(uuid4()),
        "user_message": request.message,

        "customer_name": request.customer_name,
        "contact_number": request.contact_number,



        "intent": None,
        "selected_agent": None,
        "agent_response": None,
        "lead_data": None,


        "requires_human_approval": False,
        "next_step": None,
    }

    result = agent_graph.invoke(initial_state)

    return {
        "conversation_id": result["conversation_id"],
        "tenant_id": result["tenant_id"],
        "selected_agent": result["selected_agent"],
        "intent": result["intent"],
        "response": result["agent_response"],
        "lead_id": result.get("lead_id"),
        
        "lead_data": result["lead_data"],
        "requires_human_approval": result["requires_human_approval"],
    }




