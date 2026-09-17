from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import events, users

app = FastAPI(
    title="Event Ticket Booking Service",
    description="A minimal service for booking event tickets.",
    version="0.1.0",
)

app.include_router(events.router)
app.include_router(users.router)

static_dir = Path(__file__).parent / "static"
app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="ui")


@app.get("/health")
def health_check():
    return {"status": "ok"}
