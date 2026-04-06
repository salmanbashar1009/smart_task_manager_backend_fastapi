from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr

    class config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str