from fastapi import Depends

from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
)
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.firebase.repositories.firebase_user_repository import (
    FirebaseUserRepository,
)


def get_user_repository() -> UserRepository:
    return FirebaseUserRepository()


def get_create_user_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def get_get_user_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> GetUserUseCase:
    return GetUserUseCase(repo)


def get_list_users_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> ListUsersUseCase:
    return ListUsersUseCase(repo)


def get_update_user_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


def get_delete_user_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)
