from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class LogIngest(BaseModel):
    raw_log: str
    log_type: Optional[str] = "auto"

class LogOut(BaseModel):
    id: int
    timestamp: Optional[datetime] = None
    source_ip: str
    destination_ip: Optional[str] = None
    event_type: str
    severity: str
    raw_message: str
    parsed_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)