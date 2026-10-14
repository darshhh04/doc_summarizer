from typing import List, Optional
from pydantic import BaseModel, Field


class Decision(BaseModel):
    decision: str
    made_by: str = "Unknown"        


class ActionItem(BaseModel):
    task: str
    owner: str = "Unassigned"
    deadline: Optional[str] = None


class Risk(BaseModel):
    risk: str
    severity: str = Field(description="Low, Medium or High")


class Topic(BaseModel):
    name: str
    points: List[str] = []


class MeetingResult(BaseModel):
    summary: str
    decisions: List[Decision] = []
    action_items: List[ActionItem] = []
    risks: List[Risk] = []
    topics: List[Topic] = []



class DecisionList(BaseModel):
    decisions: List[Decision] = []


class ActionItemList(BaseModel):
    action_items: List[ActionItem] = []


class RiskList(BaseModel):
    risks: List[Risk] = []


class TopicList(BaseModel):
    topics: List[Topic] = []