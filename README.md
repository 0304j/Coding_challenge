# Event Ticket Booking Service

Ein einfacher REST-Service mit FastAPI: Nutzer sehen Events und buchen Tickets, der Owner
verwaltet Events. Kein User-Management — die User-ID wird einfach mitgeschickt.

## Projektstruktur

```
app/
  main.py           # FastAPI-App, bindet Router + Test-UI ein
  schemas.py        # Pydantic-Modelle (Event, Ticket, ...)
  storage.py        # In-Memory "Datenbank"
  routers/
    events.py       # /events Endpunkte (auflisten, anlegen, löschen, buchen, Buchungsanzahl)
    users.py         # /users/{id}/tickets Endpunkt
  static/
    index.html      # kleine Test-UI im Browser
docker/
  Dockerfile
requirements.txt
```

## Starten – drei Möglichkeiten

### 1. Docker-Image von Docker Hub pullen
```bash
docker pull arnoldt04/stackit-ticket-service:latest
docker run -d -p 8000:8000 arnoldt04/stackit-ticket-service:latest
```

### 2. Mit dem Dockerfile selbst bauen
```bash
docker build -f docker/Dockerfile -t stackit-ticket-service .
docker run -d -p 8000:8000 stackit-ticket-service
```

### 3. Lokal ohne Docker
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Danach erreichbar unter:
- API: http://127.0.0.1:8000
- Swagger-Docs: http://127.0.0.1:8000/docs
- Test-UI (einfache HTML-Seite zum Klicken): http://127.0.0.1:8000/ui/

## Beispiel-Requests

```bash
# Event anlegen (Owner)
curl -X POST http://127.0.0.1:8000/events \
  -H "Content-Type: application/json" \
  -d '{"name":"Event1","event_date":"2123-01-04","total_tickets":2}'

# Alle Events sehen (User)
curl http://127.0.0.1:8000/events

# Ticket buchen (User)
curl -X POST http://127.0.0.1:8000/events/1/bookings \
  -H "Content-Type: application/json" \
  -d '{"user_id":"alice"}'

# Eigene Tickets sehen (User)
curl http://127.0.0.1:8000/users/alice/tickets

# Buchungsanzahl für ein Event (Owner)
curl http://127.0.0.1:8000/events/1/bookings

# Event löschen (Owner)
curl -X DELETE http://127.0.0.1:8000/events/1
```

## Annahmen

- Keine Authentifizierung: Owner-Endpunkte (Event anlegen/löschen, Buchungsanzahl) sind
  nicht extra geschützt, da laut Aufgabenstellung kein User-Management gefordert ist.
- Daten liegen nur im Arbeitsspeicher (kein DB-Setup nötig) — nach Neustart sind sie weg.
  TODO: durch eine echte Datenbank ersetzen.
- Ein Event hat ein festes Ticketkontingent (`total_tickets`), `available_tickets` sinkt
  bei jeder Buchung; bei 0 verfügbaren Tickets gibt es `409 Conflict`.
