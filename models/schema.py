from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ParsedQuery(BaseModel):
    sport: str
    timeframe: str

class Match(BaseModel):
    team1: str
    team2: str
    start_time: datetime
    sport: str
    competition: Optional[str] = None

class ScheduledEvent(BaseModel):
    event_id: str
    summary: str
    start_time: datetime
    end_time: datetime
    status: str

class WorkflowState(BaseModel):
    query: str
    parsed_query: Optional[ParsedQuery] = None
    matches: List[Match] = Field(default_factory=list)
    favorite_teams: List[str] = Field(default_factory=list)
    filtered_matches: List[Match] = Field(default_factory=list)
    scheduled_events: List[ScheduledEvent] = Field(default_factory=list)
    error: Optional[str] = None
    status: str = "pending"