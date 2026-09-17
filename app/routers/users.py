from fastapi import APIRouter

from app.schemas import Ticket
from app.storage import tickets

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/tickets", response_model=list[Ticket])
def list_my_tickets(user_id: str):
    """A user sees all of their booked tickets."""
    return tickets.list_for_user(user_id)
