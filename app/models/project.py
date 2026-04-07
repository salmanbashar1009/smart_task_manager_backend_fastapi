from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task
    from .user import User

class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None

    # === Ownership ===
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", 
        nullable=False, 
        index=True
    )
    
    owner: Mapped["User"] = Relationship(back_populates="projects")

    tasks: Mapped[List["Task"]] = Relationship(back_populates="project")