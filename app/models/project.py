from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    # Add any other fields you have...

    tasks: Mapped[List["Task"]] = Relationship(back_populates="project")