from sqlmodel import SQLModel, Field, Relationship
import uuid
from .task import Task
from .comment import Comment
from typing import List


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True,index=True, nullable=False)
    hashed_password : str
    role: str = Field(default='member') # admin or member

    # Relationship
    tasks:List['Task'] = Relationship(back_populates= "assignee")
    comments: List["Comment"] = Relationship(back_populates="user")