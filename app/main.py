
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.api.routes import router
from app.scheduler.scheduler import start_scheduler

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Competitor Monitor",
    version="1.0.0"
)

# Start scheduler when application starts
@app.on_event("startup")
def startup_event():
    start_scheduler()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML Templates
templates = Jinja2Templates(directory="app/templates")

# API Routes
app.include_router(router)