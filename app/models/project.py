from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Any, List
from datetime import datetime
import uuid
from __future__ import annotations
from .task import Task


class Project(SQLModel,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None

    # Relationship
    tasks: List[Task] = Relationship(back_populates='project')