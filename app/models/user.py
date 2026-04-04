from typing import List
from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str
    role: str = Field(default="member")

    tasks: Mapped[List["Task"]] = Relationship(back_populates="assignee")
    comments: Mapped[List["Comment"]] = Relationship(back_populates="user")