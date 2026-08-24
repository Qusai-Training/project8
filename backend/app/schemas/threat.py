from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ThreatOut(BaseModel):
    id: int
    log_id: int
    threat_type: str
    threat_score: float
    description: str
    is_resolved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ThreatStats(BaseModel):
    total_threats: int
    low: int
    medium: int
    high: int
    critical: int