from fastapi import APIRouter
from app.api import ws, ingest, logs, threats, analytics, pfsense

api_router = APIRouter()
api_router.include_router(ws.router, tags=["websocket"])
api_router.include_router(ingest.router, prefix="/api/ingest", tags=["ingest"])
api_router.include_router(logs.router, prefix="/api/logs", tags=["logs"])
api_router.include_router(threats.router, prefix="/api/threats", tags=["threats"])
api_router.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
api_router.include_router(pfsense.router, prefix="/api/pfsense", tags=["pfsense"])
