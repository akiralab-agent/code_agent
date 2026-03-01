from typing import List

from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from src.domain.entities.user import User
from src.domain.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from src.domain.repositories.user_repository import UserRepository


def _to_response_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    async def execute(self, dto: CreateUserDTO) -> UserResponseDTO:
        existing = await self._repo.find_by_email(dto.email)
        if existing:
            raise EntityAlreadyExistsException("User", dto.email)

        user = User(name=dto.name, email=dto.email)
        saved = await self._repo.save(user)
        return _to_response_dto(saved)


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    async def execute(self, user_id: str) -> UserResponseDTO:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)
        return _to_response_dto(user)


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    async def execute(self) -> List[UserResponseDTO]:
        users = await self._repo.find_all()
        return [_to_response_dto(u) for u in users]


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    async def execute(self, user_id: str, dto: UpdateUserDTO) -> UserResponseDTO:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)

        if dto.email and dto.email != user.email:
            existing = await self._repo.find_by_email(dto.email)
            if existing:
                raise EntityAlreadyExistsException("User", dto.email)

        user.update(name=dto.name, email=dto.email)
        updated = await self._repo.update(user)
        return _to_response_dto(updated)


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repo = user_repository

    async def execute(self, user_id: str) -> None:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id)
        await self._repo.delete(user_id)
