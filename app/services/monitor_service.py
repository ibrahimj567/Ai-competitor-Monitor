from datetime import datetime

from app.crawler.playwright_engine import PlaywrightEngine

from app.database.models import Snapshot

from app.services.content_service import ContentService
from app.services.snapshot_service import SnapshotService
from app.services.diff_service import DiffService
from app.services.ai_service import AIService


class MonitorService:

    def __init__(self, db):

        self.db = db

        self.engine = PlaywrightEngine()

        self.content = ContentService()

        self.snapshot_service = SnapshotService(db)

        self.diff = DiffService()

        self.ai = AIService()

    def scan(self, website):

        # Crawl website
        result = self.engine.fetch(
            website.id,
            website.url
        )

        # Extract clean text
        cleaned = self.content.save_clean_content(
            website.id,
            result["html"]
        )

        # Get previous snapshot
        previous = self.snapshot_service.latest_snapshot(
            website.id
        )

        diff_text = ""

        ai_summary = None

        confidence = None
        severity = None

        if previous:

            diff_text = self.diff.compare_files(
                previous.clean_file,
                cleaned["path"]
            )

            if diff_text.strip():

                ai_result = self.ai.summarize_changes(
                    diff_text
                )

                ai_summary = ai_result["summary"]

                severity = ai_result["severity"]

                confidence = str(
                    ai_result["confidence"]
                )

        else:

            ai_summary = "Initial baseline scan completed."

            severity = "None"

            confidence = "1.0"

        snapshot = Snapshot(

            website_id=website.id,

            html_file=result["html_file"],

            clean_file=cleaned["path"],

            screenshot_file=result["screenshot"],

            diff_text=diff_text,

            ai_summary=ai_summary,
            
            severity=severity,

            confidence_score=confidence,

            scan_status="Completed"

        )

        self.snapshot_service.save(
            snapshot
        )

        return snapshot