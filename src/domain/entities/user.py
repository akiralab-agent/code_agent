from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    name: str
    email: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def update(self, name: Optional[str] = None, email: Optional[str] = None) -> None:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
        )
        user.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            user.updated_at = datetime.fromisoformat(data["updated_at"])
        return user
