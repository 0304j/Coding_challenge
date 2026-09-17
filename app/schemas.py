from datetime import date, datetime

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    """Payload for the owner to create a new event."""

    name: str
    event_date: date
    total_tickets: int = Field(gt=0)


class Event(BaseModel):
    """An event as stored and returned by the API."""

    id: int
    name: str
    event_date: date
    total_tickets: int
    available_tickets: int


class BookingCreate(BaseModel):
    """Payload for a user booking a ticket."""

    user_id: str


class Ticket(BaseModel):
    """A booked ticket as stored and returned by the API."""

    id: int
    event_id: int
    user_id: str
    booked_at: datetime


class EventBookingCount(BaseModel):
    """Owner view of how many tickets are booked for an event."""

    event_id: int
    event_name: str
    booked_tickets: int
