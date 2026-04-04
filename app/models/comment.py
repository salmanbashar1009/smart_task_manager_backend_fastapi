from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

# Avoid circular imports at runtime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task
    from .user import User

class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    task_id: uuid.UUID = Field(foreign_key="task.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")

    task: Mapped[Optional["Task"]] = Relationship(back_populates="comments")
    user: Mapped[Optional["User"]] = Relationship(back_populates="comments")