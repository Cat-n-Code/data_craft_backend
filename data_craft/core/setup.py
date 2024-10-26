import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from data_craft.core.db_manager import DatabaseManager  # isort: split

from data_craft.auth.routers import auth_router
from data_craft.auth.services import AuthService, PasswordService, TokenService
from data_craft.core.exceptions import (
    AppException,
    handle_app_exception,
    handle_validation_exception,
)
from data_craft.core.settings import AppSettings
from data_craft.file_entities.repositories import FileEntityRepository
from data_craft.file_entities.routers import file_entities_router
from data_craft.file_entities.services import FileEntityService
from data_craft.users.repositories import UserRepository
from data_craft.users.routers import users_router
from data_craft.users.services import UserService


def create_app(settings: AppSettings | None = None) -> FastAPI:
    if settings is None:
        settings = AppSettings()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    app = FastAPI(
        title="Сервис-конструктор отчетов",
        lifespan=_app_lifespan,
        servers=[
            {"url": "http://localhost:8888", "description": "Локальный сервер"},
            # {"url": "http://176.109.107.222:8080", "description": "Dev сервер"},
        ],
        responses={
            400: {"description": "Неверный формат входных данных"},
        },
    )

    """ Setup global dependencies """
    _setup_app_dependencies(app, settings)

    """ Setup middlewares """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    """ Setup routers """
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(file_entities_router)

    """ Setup exception handlers """
    app.add_exception_handler(AppException, handle_app_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_exception)

    return app


def _setup_app_dependencies(app: FastAPI, settings: AppSettings):
    app.state.settings = settings
    app.state.database_manager = DatabaseManager(settings.db_url)

    user_repository = UserRepository()
    file_entity_repository = FileEntityRepository()

    password_service = PasswordService()
    password_service = PasswordService()
    token_service = TokenService(
        settings.auth_token_secret_key, settings.auth_token_lifetime
    )
    auth_service = AuthService(password_service, token_service, user_repository)
    user_service = UserService(password_service, user_repository)
    file_entity_service = FileEntityService(
        settings.region,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.bucket_name,
        settings.aws_endpoint,
        settings.aws_access_domain_name,
        file_entity_repository,
    )
    app.state.auth_service = auth_service
    app.state.user_service = user_service
    app.state.file_entity_service = file_entity_service


@asynccontextmanager
async def _app_lifespan(app: FastAPI):
    # settings: AppSettings = app.state.settings
    db: DatabaseManager = app.state.database_manager

    await db.initialize()

    # if settings.initial_user is not None:
    #     user_service: UserService = app.state.user_service
    #     async with db.create_session() as session:
    #         try:
    #             await user_service.create(session, settings.initial_user)
    #             logging.info("Initial user was successfully created")
    #         except EntityAlreadyExistsException:
    #             logging.info("Initial user already exists. Skipped")

    yield
    await db.dispose()
