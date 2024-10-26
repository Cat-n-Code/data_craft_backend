from fastapi import APIRouter, Depends, status

from data_craft.auth.dependencies import HasPermission
from data_craft.auth.permissions import Anonymous
from data_craft.auth.schemas import AuthTokenSchema, LoginCredentials
from data_craft.core.dependencies import AuthServiceDep, DbSession

auth_router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@auth_router.post(
    "/login",
    summary="Метод аутентификации пользователя",
    response_model=AuthTokenSchema,
    response_description=(
        "`token` - уникальный токен, действующий определенное время. "
        "Необходим для авторизации в других методах."
    ),
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Указанные `email` или `password` не верные"
        },
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь уже авторизован"},
    },
    dependencies=[Depends(HasPermission(Anonymous()))],
)
async def login(
    session: DbSession, auth_service: AuthServiceDep, schema: LoginCredentials
):
    return await auth_service.login_user(session, schema)
