from fastapi import APIRouter, Query
from sqlalchemy import select, func
from typing import Optional, List
from datetime import datetime
from app.database.connection import engine
from app.database.tables import threat_alerts
from app.schemas.threat import ThreatOut, ThreatStats

router = APIRouter()

@router.get("", response_model=List[ThreatOut])
def get_threats(
    severity: Optional[str] = Query(None, description="Filter by severity: Low, Medium, High, Critical"),
    from_date: Optional[datetime] = Query(None, description="Filter start date"),
    to_date: Optional[datetime] = Query(None, description="Filter end date")
):
    with engine.connect() as conn:
        query = select(threat_alerts)
        if severity:
            query = query.where(threat_alerts.c.threat_type == severity)
        if from_date:
            query = query.where(threat_alerts.c.created_at >= from_date)
        if to_date:
            query = query.where(threat_alerts.c.created_at <= to_date)
            
        result = conn.execute(query.order_by(threat_alerts.c.created_at.desc())).fetchall()
        return [dict(row._mapping) for row in result]

@router.get("/stats", response_model=ThreatStats)
def get_threat_stats():
    with engine.connect() as conn:
        query = select(
            threat_alerts.c.threat_type,
            func.count(threat_alerts.c.id).label("count")
        ).group_by(threat_alerts.c.threat_type)
        
        result = conn.execute(query).fetchall()
        stats = {row.threat_type: row.count for row in result}
        return ThreatStats(
            total_threats=sum(stats.values()),
            low=stats.get("Low", 0),
            medium=stats.get("Medium", 0),
            high=stats.get("High", 0),
            critical=stats.get("Critical", 0)
        )