from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import Snapshot


class SnapshotService:

    def __init__(self, db: Session):

        self.db = db

    # =====================================================
    # Save Snapshot
    # =====================================================

    def save(self, snapshot: Snapshot):

        self.db.add(snapshot)

        self.db.commit()

        self.db.refresh(snapshot)

        return snapshot

    # =====================================================
    # Get Snapshot by ID
    # =====================================================

    def get(self, snapshot_id: int):

        return (
            self.db.query(Snapshot)
            .filter(
                Snapshot.id == snapshot_id
            )
            .first()
        )

    # =====================================================
    # Get Latest Snapshot
    # =====================================================

    def latest_snapshot(self, website_id: int):

        return (
            self.db.query(Snapshot)
            .filter(
                Snapshot.website_id == website_id
            )
            .order_by(
                Snapshot.created_at.desc()
            )
            .first()
        )

    # =====================================================
    # Get Previous Snapshot
    # =====================================================

    def previous_snapshot(self, website_id: int):

        snapshots = (
            self.db.query(Snapshot)
            .filter(
                Snapshot.website_id == website_id
            )
            .order_by(
                Snapshot.created_at.desc()
            )
            .limit(2)
            .all()
        )

        if len(snapshots) < 2:
            return None

        return snapshots[1]

    # =====================================================
    # Get All Snapshots for Website
    # =====================================================

    def get_by_website(self, website_id: int):

        return (
            self.db.query(Snapshot)
            .filter(
                Snapshot.website_id == website_id
            )
            .order_by(
                Snapshot.created_at.desc()
            )
            .all()
        )

    # =====================================================
    # Delete Snapshot
    # =====================================================

    def delete(self, snapshot_id: int):

        snapshot = self.get(snapshot_id)

        if snapshot:

            self.db.delete(snapshot)

            self.db.commit()

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    def total_scans(self):

        return (
            self.db.query(Snapshot)
            .count()
        )

    # =====================================================
    # Today's Scans
    # =====================================================

    def scans_today(self):

        today = datetime.utcnow().date()

        return (
            self.db.query(Snapshot)
            .filter(
                Snapshot.created_at >= today
            )
            .count()
        )

    # =====================================================
    # High Severity Alerts
    # =====================================================

    def high_alerts(self):

        return (
            self.db.query(Snapshot)
            .filter(
                Snapshot.severity == "High"
            )
            .count()
        )

    # =====================================================
    # Latest Scan
    # =====================================================

    def latest_scan(self):

        return (
            self.db.query(Snapshot)
            .order_by(
                Snapshot.created_at.desc()
            )
            .first()
        )