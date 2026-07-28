from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler.jobs import scheduled_scan

scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        scheduled_scan,
        trigger="interval",
        minutes=1,
        id="scheduler",
        replace_existing=True,
    )

    scheduler.start()

    print("✅ Scheduler Started")