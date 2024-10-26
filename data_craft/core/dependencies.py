from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from data_craft.auth.services import AuthService
from data_craft.core.db_manager import DatabaseManager
from data_craft.file_entities.services import FileEntityService
from data_craft.users.services import UserService


def db_manager(request: Request) -> DatabaseManager:
    return request.app.state.database_manager


async def db_session(db_manager: Annotated[DatabaseManager, Depends(db_manager)]):
    async with db_manager.create_session() as session:
        yield session


def auth_service(request: Request) -> AuthService:
    return request.app.state.auth_service


def user_service(request: Request) -> UserService:
    return request.app.state.user_service

def file_entity_service(request: Request) -> FileEntityService:
    return request.app.state.file_entity_service



DbSession = Annotated[AsyncSession, Depends(db_session)]
AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
UserServiceDep = Annotated[UserService, Depends(user_service)]
FileEntityServiceDep = Annotated[FileEntityService, Depends(file_entity_service)]