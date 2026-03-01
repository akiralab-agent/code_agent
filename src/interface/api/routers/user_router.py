from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
)
from src.domain.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from src.interface.api.dependencies.user_dependencies import (
    get_create_user_use_case,
    get_delete_user_use_case,
    get_get_user_use_case,
    get_list_users_use_case,
    get_update_user_use_case,
)
from src.interface.api.schemas.user_schema import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def create_user(
    body: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponse:
    try:
        result = await use_case.execute(CreateUserDTO(name=body.name, email=body.email))
        return UserResponse(**result.__dict__)
    except EntityAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=e.message)


@router.get("", response_model=List[UserResponse])
async def list_users(
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
) -> List[UserResponse]:
    results = await use_case.execute()
    return [UserResponse(**r.__dict__) for r in results]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
) -> UserResponse:
    try:
        result = await use_case.execute(user_id)
        return UserResponse(**result.__dict__)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.message)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    body: UpdateUserRequest,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
) -> UserResponse:
    try:
        result = await use_case.execute(
            user_id, UpdateUserDTO(name=body.name, email=body.email)
        )
        return UserResponse(**result.__dict__)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.message)
    except EntityAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=e.message)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(
    user_id: str,
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
) -> None:
    try:
        await use_case.execute(user_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.message)
