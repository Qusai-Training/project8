from fastapi import APIRouter
from sqlalchemy import select, func
from app.database.connection import engine
from app.database.tables import logs, threat_alerts
from app.schemas.analytics import AnalyticsTimeline

router = APIRouter()

@router.get("/timeline", response_model=AnalyticsTimeline)
def get_analytics_timeline():
    with engine.connect() as conn:
        log_counts = conn.execute(
            select(
                func.date_trunc('hour', logs.c.created_at).label('timestamp'),
                func.count().label('event_count')
            ).group_by('timestamp').order_by('timestamp')
        ).fetchall()
        
        threat_counts = conn.execute(
            select(
                func.date_trunc('hour', threat_alerts.c.created_at).label('timestamp'),
                func.count().label('event_count')
            ).group_by('timestamp').order_by('timestamp')
        ).fetchall()
        
        return AnalyticsTimeline(
            logs_timeline=[dict(row._mapping) for row in log_counts],
            threats_timeline=[dict(row._mapping) for row in threat_counts]
        )