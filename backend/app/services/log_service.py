from sqlalchemy import insert
from app.database.connection import engine
from app.database.tables import logs, threat_alerts
from app.parsers.log_parser import parse_log
from app.detection.threat_detector import evaluate_threats
from app.websocket.manager import manager

async def process_incoming_log(raw_message: str, force_format: str = "auto") -> dict:
    """End-to-end ingestion and alert pipeline."""
    # 1. Parse incoming log payload
    parsed = parse_log(raw_message, force_format=force_format)

    # 2. Save log record into Database via SQLAlchemy Core
    with engine.begin() as conn:
        result = conn.execute(insert(logs).values(**parsed))
        log_id = result.inserted_primary_key[0]
        parsed["id"] = log_id

    # 3. Broadcast new_log event to connected WebSocket clients
    await manager.broadcast("new_log", parsed)

    # 4. Execute threat detection logic
    threat = evaluate_threats(parsed)
    if threat:
        threat_record = {
            "log_id": log_id,
            "threat_type": threat["threat_type"],
            "threat_score": threat["threat_score"],
            "description": threat["description"],
            "is_resolved": False
        }
        
        # 5. Persist threat alert into Database
        with engine.begin() as conn:
            alert_result = conn.execute(insert(threat_alerts).values(**threat_record))
            threat_record["id"] = alert_result.inserted_primary_key[0]

        # 6. Broadcast threat_alert event live via WebSockets
        await manager.broadcast("threat_alert", threat_record)

    return parsed