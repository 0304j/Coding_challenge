"""In-memory data store.

TODO: replace with a real database (e.g. PostgreSQL via SQLAlchemy) for
persistence across restarts and concurrent-safe access.
"""

from datetime import datetime, timezone
from itertools import count
from typing import Dict, List, Optional

from app.schemas import Event, EventCreate, Ticket


class EventRepository:
    def __init__(self) -> None:
        self._events: Dict[int, Event] = {}
        self._ids = count(1)

    def create(self, data: EventCreate) -> Event:
        event_id = next(self._ids)
        event = Event(
            id=event_id,
            name=data.name,
            event_date=data.event_date,
            total_tickets=data.total_tickets,
            available_tickets=data.total_tickets,
        )
        self._events[event_id] = event
        return event

    def list_all(self) -> List[Event]:
        return list(self._events.values())

    def get(self, event_id: int) -> Optional[Event]:
        return self._events.get(event_id)

    def delete(self, event_id: int) -> bool:
        return self._events.pop(event_id, None) is not None

    def decrement_availability(self, event_id: int) -> None:
        event = self._events[event_id]
        event.available_tickets -= 1


class TicketRepository:
    def __init__(self) -> None:
        self._tickets: Dict[int, Ticket] = {}
        self._ids = count(1)

    def create(self, event_id: int, user_id: str) -> Ticket:
        ticket_id = next(self._ids)
        ticket = Ticket(
            id=ticket_id,
            event_id=event_id,
            user_id=user_id,
            booked_at=datetime.now(timezone.utc),
        )
        self._tickets[ticket_id] = ticket
        return ticket

    def list_for_user(self, user_id: str) -> List[Ticket]:
        return [t for t in self._tickets.values() if t.user_id == user_id]

    def count_for_event(self, event_id: int) -> int:
        return sum(1 for t in self._tickets.values() if t.event_id == event_id)

    def delete_for_event(self, event_id: int) -> None:
        stale = [tid for tid, t in self._tickets.items() if t.event_id == event_id]
        for tid in stale:
            del self._tickets[tid]


# Module-level singletons shared across the app (simple in-memory "DB").
events = EventRepository()
tickets = TicketRepository()
