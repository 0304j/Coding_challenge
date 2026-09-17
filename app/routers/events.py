from fastapi import APIRouter, HTTPException, status

from app.schemas import BookingCreate, Event, EventBookingCount, EventCreate, Ticket
from app.storage import events, tickets

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[Event])
def list_events():
    """A user sees all available events."""
    return events.list_all()


@router.post("", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(data: EventCreate):
    """The owner adds a new event."""
    return events.create(data)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int):
    """The owner deletes an event."""
    if not events.delete(event_id):
        raise HTTPException(status_code=404, detail="Event not found")
    tickets.delete_for_event(event_id)


@router.post(
    "/{event_id}/bookings", response_model=Ticket, status_code=status.HTTP_201_CREATED
)
def book_ticket(event_id: int, data: BookingCreate):
    """A user books a ticket for an event."""
    event = events.get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.available_tickets <= 0:
        raise HTTPException(status_code=409, detail="No tickets available for this event")

    events.decrement_availability(event_id)
    return tickets.create(event_id=event_id, user_id=data.user_id)


@router.get("/{event_id}/bookings", response_model=EventBookingCount)
def get_booking_count(event_id: int):
    """The owner sees how many tickets are booked for a specific event."""
    event = events.get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return EventBookingCount(
        event_id=event.id,
        event_name=event.name,
        booked_tickets=tickets.count_for_event(event_id),
    )
