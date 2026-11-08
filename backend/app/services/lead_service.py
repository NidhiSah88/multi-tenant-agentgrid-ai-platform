
# from uuid import uuid4
# from datetime import datetime, timezone
# # Temporary storage/ in memory storage . PostgreSQL will replace this.
# leads = {}


# def create_lead(tenant_id: str, customer_name: str, contact_number: str):
#     lead_id = str(uuid4())

#     lead = {
#         "lead_id": lead_id,
#         "tenant_id": tenant_id,
#         "customer_name": customer_name,
#         "contact_number": contact_number,
#         "status": "pending_approval",
#         "created_at": datetime.now(timezone.utc).isoformat(),
#     }
    
#     # Every time you create a lead, this line stores it:
#     leads[lead_id] = lead
    
#     return lead


# def get_pending_leads(tenant_id: str):
#     return [
#         lead for lead in leads.values()
#         if lead["tenant_id"] == tenant_id
#         and lead["status"] == "pending_approval"
#     ]


# def update_lead_status(lead_id: str, status: str, tenant_id: str):
#     lead = leads.get(lead_id)

#     if not lead or lead["tenant_id"] != tenant_id:
#         return None

#     lead["status"] = status
#     return lead



# this file has been updated to use PostgreSQL for lead storage 
# instead of in-memory storage. The new implementation uses SQLAlchemy 
# to interact with the database, providing functions to create leads,
#  retrieve pending leads, and update lead statuses.



# What changed?
# - create_lead() now inserts records into PostgreSQL.
# - get_pending_leads() retrieves pending records from PostgreSQL.
# - update_lead_status() updates the database record.
# - Tenant filtering is preserved, so one tenant cannot access another tenant's leads through these functions.



from uuid import uuid4

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models import Lead


def lead_to_dict(lead: Lead) -> dict:
    """Convert a Lead database model into a JSON-friendly dictionary."""
    return {
        "lead_id": lead.lead_id,
        "tenant_id": lead.tenant_id,
        "customer_name": lead.customer_name,
        "contact_number": lead.contact_number,
        "status": lead.status,
        "created_at": lead.created_at.isoformat(),
    }


def create_lead(
    tenant_id: str,
    customer_name: str,
    contact_number: str,
):
    """Create and persist a new lead in PostgreSQL."""

    with SessionLocal() as db:
        try:
            lead = Lead(
                lead_id=str(uuid4()),
                tenant_id=tenant_id,
                customer_name=customer_name,
                contact_number=contact_number,
                status="pending_approval",
            )

            db.add(lead)
            db.commit()
            db.refresh(lead)

            return lead_to_dict(lead)

        except Exception:
            db.rollback()
            raise


def get_pending_leads(tenant_id: str):
    """Get pending approval leads for a specific tenant."""

    with SessionLocal() as db:
        statement = (
            select(Lead)
            .where(
                Lead.tenant_id == tenant_id,
                Lead.status == "pending_approval",
            )
            .order_by(Lead.created_at.desc())
        )

        leads = db.scalars(statement).all()

        return [lead_to_dict(lead) for lead in leads]


def update_lead_status(
    lead_id: str,
    status: str,
    tenant_id: str,
):
    """Approve or reject a lead belonging to the specified tenant."""

    with SessionLocal() as db:
        try:
            statement = select(Lead).where(
                Lead.lead_id == lead_id,
                Lead.tenant_id == tenant_id,
            )

            lead = db.scalar(statement)

            if not lead:
                return None

            lead.status = status

            db.commit()
            db.refresh(lead)

            return lead_to_dict(lead)

        except Exception:
            db.rollback()
            raise








