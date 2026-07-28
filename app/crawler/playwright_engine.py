from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright


class PlaywrightEngine:

    def fetch(self, website_id: int, url: str):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        base = Path("storage") / f"website_{website_id}"

        html_dir = base / "html"
        screenshot_dir = base / "screenshots"

        html_dir.mkdir(parents=True, exist_ok=True)
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        html_file = html_dir / f"{timestamp}.html"
        screenshot_file = screenshot_dir / f"{timestamp}.png"

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page(
                viewport={
                    "width": 1440,
                    "height": 900
                }
            )

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(3000)

            page.screenshot(
                path=str(screenshot_file),
                full_page=True
            )

            html = page.content()

            html_file.write_text(
                html,
                encoding="utf-8"
            )

            browser.close()

        return {
            "html": html,
            "html_file": str(html_file),
            "screenshot": str(screenshot_file)
        }