from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime
from typing import TYPE_CHECKING 
if TYPE_CHECKING:
    from .user import User
    from .project import Project
    from .comment import Comment

#---

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="todo")
    created_at: datetime = Field(default_factory=datetime.now)

    project_id: Optional[uuid.UUID] = Field(default=None, foreign_key="project.id")
    assignee_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    project: Mapped[Optional["Project"]] = Relationship(back_populates="tasks")
    assignee: Mapped[Optional["User"]] = Relationship(back_populates="tasks")
    comments: Mapped[List["Comment"]] = Relationship(back_populates="task")