from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: str

    class config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str