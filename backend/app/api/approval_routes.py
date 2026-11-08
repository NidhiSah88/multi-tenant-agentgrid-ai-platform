
from fastapi import APIRouter, HTTPException
from app.services.lead_service import (
    get_pending_leads,
    update_lead_status,
)

router = APIRouter()


@router.get("/pending")
async def pending_approvals(tenant_id: str = "demo-tenant"):

    return {
        "pending_leads": get_pending_leads(tenant_id)
    }


@router.post("/{lead_id}/approve")
async def approve_lead(lead_id: str, tenant_id: str = "demo-tenant"):

    lead = update_lead_status(
        lead_id,
        "approved",
        tenant_id,
    )

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {
        "message": "Appointment request approved",
        "lead": lead,
    }


@router.post("/{lead_id}/reject")
async def reject_lead(lead_id: str, tenant_id: str = "demo-tenant"):

    lead = update_lead_status(
        lead_id,
        "rejected",
        tenant_id,
    )

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {
        "message": "Appointment request rejected",
        "lead": lead,
    }






