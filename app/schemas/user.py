from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: str

    class config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str