from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Optional[str] = Field(default="member", pattern="^(member|admin)$")


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: str

    class config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str