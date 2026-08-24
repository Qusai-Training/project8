from fastapi import APIRouter
from sqlalchemy import select, func
from typing import List
from app.database.connection import engine
from app.database.tables import logs
from app.schemas.analytics import FirewallRuleHit

router = APIRouter()

@router.get("/firewall-rules", response_model=List[FirewallRuleHit])
def get_pfsense_firewall_rules():
    with engine.connect() as conn:
        query = select(
            logs.c.event_type,
            func.count(logs.c.id).label("hits")
        ).where(logs.c.raw_message.like("%pfsense%")).group_by(logs.c.event_type)
        
        result = conn.execute(query).fetchall()
        return [dict(row._mapping) for row in result]