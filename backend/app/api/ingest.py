from fastapi import APIRouter
from app.schemas.log import LogIngest, LogOut
from app.services.log_service import process_incoming_log

router = APIRouter()

@router.post("/log", response_model=LogOut)
async def ingest_log(payload: LogIngest):
    log_record = await process_incoming_log(payload.raw_log, force_format=payload.log_type or "auto")
    return log_record

@router.post("/pfsense", response_model=LogOut)
async def ingest_pfsense(raw_log: str):
    log_record = await process_incoming_log(raw_log, force_format="pfsense")
    return log_record