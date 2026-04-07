from typing import List
from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
import uuid

from app.models.task import Task
from app.models.comment import Comment

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str

    # === Releationship ===
    projects: Mapped[List["Projects"]] = Relationship(back_populates= "owner")

    tasks: Mapped[List["Task"]] = Relationship(back_populates="assignee")
    comments: Mapped[List["Comment"]] = Relationship(back_populates="user")
