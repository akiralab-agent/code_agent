from typing import List, Optional
from unittest.mock import AsyncMock

import pytest

from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
)
from src.domain.entities.user import User
from src.domain.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from src.domain.repositories.user_repository import UserRepository


class MockUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    async def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    async def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.email == email), None)

    async def find_all(self) -> List[User]:
        return list(self._users.values())

    async def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    async def update(self, user: User) -> User:
        self._users[user.id] = user
        return user

    async def delete(self, user_id: str) -> None:
        self._users.pop(user_id, None)


@pytest.fixture
def repo() -> MockUserRepository:
    return MockUserRepository()


@pytest.mark.asyncio
async def test_create_user_success(repo: MockUserRepository) -> None:
    use_case = CreateUserUseCase(repo)
    dto = CreateUserDTO(name="Alice", email="alice@example.com")
    result = await use_case.execute(dto)

    assert result.name == "Alice"
    assert result.email == "alice@example.com"
    assert result.id is not None


@pytest.mark.asyncio
async def test_create_user_duplicate_email_raises(repo: MockUserRepository) -> None:
    use_case = CreateUserUseCase(repo)
    dto = CreateUserDTO(name="Alice", email="alice@example.com")
    await use_case.execute(dto)

    with pytest.raises(EntityAlreadyExistsException):
        await use_case.execute(dto)


@pytest.mark.asyncio
async def test_get_user_not_found_raises(repo: MockUserRepository) -> None:
    use_case = GetUserUseCase(repo)
    with pytest.raises(EntityNotFoundException):
        await use_case.execute("non-existent-id")


@pytest.mark.asyncio
async def test_update_user_success(repo: MockUserRepository) -> None:
    create_uc = CreateUserUseCase(repo)
    created = await create_uc.execute(CreateUserDTO(name="Alice", email="alice@example.com"))

    update_uc = UpdateUserUseCase(repo)
    updated = await update_uc.execute(created.id, UpdateUserDTO(name="Alice Updated"))

    assert updated.name == "Alice Updated"
    assert updated.email == "alice@example.com"


@pytest.mark.asyncio
async def test_delete_user_success(repo: MockUserRepository) -> None:
    create_uc = CreateUserUseCase(repo)
    created = await create_uc.execute(CreateUserDTO(name="Alice", email="alice@example.com"))

    delete_uc = DeleteUserUseCase(repo)
    await delete_uc.execute(created.id)

    get_uc = GetUserUseCase(repo)
    with pytest.raises(EntityNotFoundException):
        await get_uc.execute(created.id)
