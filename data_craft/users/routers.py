from fastapi import APIRouter, Depends, status

from data_craft.auth.dependencies import AuthenticateUser, HasPermission
from data_craft.auth.permissions import Authenticated
from data_craft.core.dependencies import DbSession, UserServiceDep
from data_craft.core.schemas import PageSchema
from data_craft.core.utils import IdField, PageField, SizeField
from data_craft.users.schemas import (
    UserPasswordUpdateSchema,
    UserSchema,
    UserUpdateSchema,
)

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.get(
    "/",
    summary="Получить список всех пользователей",
    response_model=PageSchema,
    # dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_all(
    session: DbSession,
    service: UserServiceDep,
    page: PageField = 0,
    size: SizeField = 10,
):
    users = await service.get_all(session, page, size)
    return PageSchema(
        total_items_count=users.total_items_count,
        items=list(map(UserSchema.model_validate, users.items)),
    )


@users_router.get(
    "/id/{user_id}",
    summary="Получить пользователя по user_id",
    response_model=UserSchema,
    # dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get(
    session: DbSession,
    service: UserServiceDep,
    user_id: IdField,
):
    user = await service.get_by_id(session, user_id)
    return UserSchema.model_validate(user)


@users_router.get(
    "/current",
    summary="Получить текущего авторизованного пользователя",
    response_model=UserSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_current_user(user: AuthenticateUser):
    return UserSchema.model_validate(user)


@users_router.put(
    "/current",
    summary="Обновить текущего авторизованного пользователя",
    response_model=UserSchema,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Другой пользователь с указанным `email` уже существует"
        }
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_current_user(
    session: DbSession,
    user_service: UserServiceDep,
    user: AuthenticateUser,
    schema: UserUpdateSchema,
):
    new_user = await user_service.update_by_id(session, user.id, schema)
    return UserSchema.model_validate(new_user)


@users_router.put(
    "/current/password",
    summary="Обновить пароль текущего авторизованного пользователя",
    response_model=UserSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_current_user_password(
    session: DbSession,
    user_service: UserServiceDep,
    user: AuthenticateUser,
    schema: UserPasswordUpdateSchema,
):
    user = await user_service.update_password_by_id(session, user.id, schema.password)
    return UserSchema.model_validate(user)
