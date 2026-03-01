from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
