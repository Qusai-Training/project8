from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class TimelinePoint(BaseModel):
    timestamp: datetime
    event_count: int

class AnalyticsTimeline(BaseModel):
    logs_timeline: List[TimelinePoint]
    threats_timeline: List[TimelinePoint]

class FirewallRuleHit(BaseModel):
    event_type: str
    hits: int