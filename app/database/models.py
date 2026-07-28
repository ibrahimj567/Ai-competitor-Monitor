from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from app.database.database import Base

class Website(Base):

    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String(500), unique=True, nullable=False)

    status = Column(String(50), default="Never Scanned")

    last_scan = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    is_active = Column(Boolean, default=True)

    scan_frequency = Column(
    Integer,
    default=60
    )   

    next_scan = Column(
    DateTime,
    nullable=True
    )

    last_scan_duration = Column(
    Float,
    default=0.0
    )

    snapshots = relationship(
        "Snapshot",
        back_populates="website",
        cascade="all, delete-orphan"
    )

    


class Snapshot(Base):

    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True)

    website_id = Column(
        Integer,
        ForeignKey("websites.id", ondelete="CASCADE"),
        nullable=False
    )

    html_file = Column(String(500))

    clean_file = Column(String(500))

    screenshot_file = Column(String(500))

    diff_text = Column(Text)

    ai_summary = Column(Text)

    severity = Column(String(20))

    confidence_score = Column(String(20))

    scan_status = Column(String(50))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    website = relationship(
        "Website",
        back_populates="snapshots"
    )