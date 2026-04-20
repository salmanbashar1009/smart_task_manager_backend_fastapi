from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    success: bool = True
    message: Literal["user created successfully"]
    model_config = {"from_attributes": True}
