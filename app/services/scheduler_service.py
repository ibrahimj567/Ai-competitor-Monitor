from datetime import datetime, timedelta
import time

from app.services.website_service import WebsiteService
from app.services.monitor_service import MonitorService


class SchedulerService:

    def __init__(self, db):

        self.db = db

        self.website_service = WebsiteService(db)

    # =====================================================
    # Scan all websites that are due
    # =====================================================

    def process_due_websites(self):

        websites = self.website_service.get_due_websites()

        if not websites:

            print("[Scheduler] No websites due.")

            return

        print(f"[Scheduler] {len(websites)} website(s) due.")

        for website in websites:

            self.run_scan(website)

    # =====================================================
    # Scan one website
    # =====================================================

    def run_scan(self, website):

        print(f"[Scheduler] Scanning {website.url}")

        start = time.perf_counter()

        try:

            monitor = MonitorService(self.db)

            monitor.scan(website)

            duration = round(
                time.perf_counter() - start,
                2
            )

            website.last_scan_duration = duration

            website.last_scan = datetime.utcnow()

            website.next_scan = (
                datetime.utcnow()
                + timedelta(
                    minutes=website.scan_frequency
                )
            )

            website.status = "Completed"

            self.db.commit()

            print(
                f"[Scheduler] Completed in {duration}s"
            )

        except Exception as e:

            website.status = "Failed"

            website.next_scan = (
                datetime.utcnow()
                +timedelta(minutes=website.scan_frequency)
            )

            self.db.commit()

            print(f"[Scheduler] ERROR: {e}")

    # =====================================================
    # Manual Scan
    # =====================================================

    def scan_now(self, website):   

        return self.run_scan(website)

