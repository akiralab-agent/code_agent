from typing import List, Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.firebase.config import get_db_reference

_COLLECTION = "users"


class FirebaseUserRepository(UserRepository):
    def __init__(self) -> None:
        self._ref = get_db_reference(_COLLECTION)

    async def find_by_id(self, user_id: str) -> Optional[User]:
        data = self._ref.child(user_id).get()
        if data is None:
            return None
        return User.from_dict(data)

    async def find_by_email(self, email: str) -> Optional[User]:
        all_users = self._ref.get() or {}
        for user_data in all_users.values():
            if user_data.get("email") == email:
                return User.from_dict(user_data)
        return None

    async def find_all(self) -> List[User]:
        all_users = self._ref.get() or {}
        return [User.from_dict(data) for data in all_users.values()]

    async def save(self, user: User) -> User:
        self._ref.child(user.id).set(user.to_dict())
        return user

    async def update(self, user: User) -> User:
        self._ref.child(user.id).update(user.to_dict())
        return user

    async def delete(self, user_id: str) -> None:
        self._ref.child(user_id).delete()
