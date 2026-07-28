from app.database.database import SessionLocal

from app.services.scheduler_service import SchedulerService


def scheduled_scan():

    db = SessionLocal()

    try:

        scheduler = SchedulerService(db)

        scheduler.process_due_websites()

    finally:

        db.close()