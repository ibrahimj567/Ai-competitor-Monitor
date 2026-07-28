from pathlib import Path
from datetime import datetime

from app.services.html_cleaner import HTMLCleaner


class ContentService:

    def __init__(self):
        self.cleaner = HTMLCleaner()

    def save_clean_content(self, website_id: int, html: str):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        base = Path("storage") / f"website_{website_id}"

        clean_dir = base / "clean"

        clean_dir.mkdir(parents=True, exist_ok=True)

        cleaned = self.cleaner.clean(html)

        file_path = clean_dir / f"{timestamp}.txt"

        file_path.write_text(
            cleaned,
            encoding="utf-8"
        )

        return {
            "text": cleaned,
            "path": str(file_path)
        }