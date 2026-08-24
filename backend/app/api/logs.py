from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import List
from app.database.connection import engine
from app.database.tables import logs
from app.schemas.log import LogOut

router = APIRouter()

@router.get("/recent", response_model=List[LogOut])
def get_recent_logs(limit: int = Query(default=50, le=500)):
    with engine.connect() as conn:
        query = select(logs).order_by(logs.c.created_at.desc()).limit(limit)
        result = conn.execute(query).fetchall()
        return [dict(row._mapping) for row in result]