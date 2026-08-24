from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database.metadata import metadata


# Core Table: logs
logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("timestamp", DateTime(timezone=True), nullable=True),
    Column("source_ip", String, index=True, nullable=False),
    Column("destination_ip", String, nullable=True),
    Column("event_type", String, index=True, nullable=False),
    Column("severity", String, nullable=False),
    Column("raw_message", String, nullable=False),
    Column("parsed_data", JSON, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

# Core Table: threat_alerts
threat_alerts = Table(
    "threat_alerts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("log_id", Integer, ForeignKey("logs.id", ondelete="CASCADE"), nullable=False),
    Column("threat_type", String, index=True, nullable=False),
    Column("threat_score", Float, nullable=False),
    Column("description", String, nullable=False),
    Column("is_resolved", Boolean, default=False, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)