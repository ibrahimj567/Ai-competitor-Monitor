from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import Website


class WebsiteService:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================
    # Get all websites
    # ==========================================

    def get_all(self):

        return (
            self.db.query(Website)
            .order_by(Website.id.desc())
            .all()
        )

    # ==========================================
    # Websites Due For Scan
    # ==========================================

    def get_due_websites(self):

        return (
            self.db.query(Website)
            .filter(
                Website.is_active == True,
                Website.next_scan <= datetime.utcnow()
            )
            .all()
        )

    # ==========================================
    # Get single website
    # ==========================================

    def get(self, website_id: int):

        return (
            self.db.query(Website)
            .filter(
                Website.id == website_id
            )
            .first()
        )

    # ==========================================
    # Get website with snapshots
    # ==========================================

    def get_with_snapshots(self, website_id: int):

        return (
            self.db.query(Website)
            .filter(
                Website.id == website_id
            )
            .first()
        )

    # ==========================================
    # Create website
    # ==========================================

    def create(self, url: str):

        # Normalize URL
        url = url.strip().lower().rstrip("/")

        # Check if already exists
        existing = (
            self.db.query(Website)
            .filter(Website.url == url)
            .first()
        )

        if existing:
            return existing

        website = Website(
            url=url
        )

        self.db.add(website)
        self.db.commit()
        self.db.refresh(website)

        return website

    # ==========================================
    # Delete website
    # ==========================================

    def delete(self, website_id: int):

        website = self.get(website_id)

        if website:

            self.db.delete(website)
            self.db.commit()

    # ==========================================
    # Update scan status
    # ==========================================

    def update_scan(
        self,
        website_id: int,
        status: str = "Scanned"
    ):

        website = self.get(website_id)

        if website:

            website.status = status
            website.last_scan = datetime.utcnow()

            self.db.commit()
            self.db.refresh(website)

        return website

    # ==========================================
    # Dashboard Statistics
    # ==========================================

    def total_websites(self):

        return (
            self.db.query(Website)
            .count()
        )

    # ==========================================
    # Active Websites
    # ==========================================

    def active_websites(self):

        return (
            self.db.query(Website)
            .filter(
                Website.is_active == True
            )
            .count()
        )