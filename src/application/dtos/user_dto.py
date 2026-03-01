from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateUserDTO:
    name: str
    email: str


@dataclass
class UpdateUserDTO:
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class UserResponseDTO:
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None
