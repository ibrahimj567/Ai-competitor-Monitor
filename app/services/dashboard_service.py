from datetime import date

from sqlalchemy import func

from app.database.models import Website, Snapshot


class DashboardService:

    def __init__(self, db):

        self.db = db

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    def get_dashboard_stats(self):

        total_websites = self.get_total_websites()

        total_scans = self.get_total_scans()

        changes_today = self.get_changes_today()

        high_alerts = self.get_high_alerts()

        average_scan_time = self.get_average_scan_time()

        next_scan = self.get_next_scan()

        return {

            "total_websites": total_websites,

            "total_scans": total_scans,

            "changes_today": changes_today,

            "high_alerts": high_alerts,

            "average_scan_time": average_scan_time,

            "next_scan": next_scan,

            "recent_activity":  self.get_recent_activity(),

        }

    # =====================================================
    # Total Websites
    # =====================================================

    def get_total_websites(self):

        return self.db.query(Website).count()

    # =====================================================
    # Total Scans
    # =====================================================

    def get_total_scans(self):

        return self.db.query(Snapshot).count()

    # =====================================================
    # Changes Today
    # =====================================================

    def get_changes_today(self):

        today = date.today()

        return (

            self.db.query(Snapshot)

            .filter(

                func.date(Snapshot.created_at) == today,

                Snapshot.diff_text.isnot(None),

                Snapshot.diff_text != ""

            )

            .count()

        )

    # =====================================================
    # High Alerts
    # =====================================================

    def get_high_alerts(self):

        return (

            self.db.query(Snapshot)

            .filter(

                Snapshot.severity == "High"

            )

            .count()

        )

    # =====================================================
    # Average Scan Time
    # =====================================================

    def get_average_scan_time(self):

        avg = (

            self.db.query(

                func.avg(

                    Website.last_scan_duration

                )

            )
            .filter(Website.last_scan.isnot(None))
            .scalar()

        )

        if avg is None:

            return "0 sec"

        return f"{round(avg,2)} sec"

    # =====================================================
    # Next Scan
    # =====================================================

    def get_next_scan(self):

        next_scan = (

            self.db.query(

                func.min(

                    Website.next_scan

                )

            )

            .filter(

                Website.is_active == True

            )

            .scalar()

        )

        if next_scan is None:

            return "No Scan Scheduled"

        return next_scan.strftime(

            "%d %b %I:%M %p"

        )
    
    def get_recent_activity(self, limit=10):

        snapshots = (
        self.db.query(Snapshot)
        .order_by(Snapshot.created_at.desc())
        .limit(limit)
        .all()
        )

        return snapshots