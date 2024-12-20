# flake8: noqa F401
import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DatabaseManager:
    def __init__(self, db_url: str):
        self._db_url = db_url

    async def initialize(self):
        try:
            self._engine = create_async_engine(self._db_url)
            self._sessionmaker = async_sessionmaker(
                self._engine, expire_on_commit=False, autoflush=False
            )
            logging.info("Successfully connected to database")
        except Exception as ex:
            logging.error(
                "Exception occurred during connection to database", exc_info=ex
            )
            raise

        """Import all used models"""
        from data_craft.file_entities.models import FileEntity
        from data_craft.users.models import User

        async with self._engine.begin() as connection:
            try:
                await connection.run_sync(Base.metadata.create_all)
                logging.info("Database tables were successfully created")
            except Exception as ex:
                logging.error(
                    "Exception occurred during database tables creation", exc_info=ex
                )
                raise

    async def dispose(self):
        await self._engine.dispose()
        logging.info("Closed connection with database")

    @asynccontextmanager
    async def create_session(self):
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as ex:
                logging.error(
                    "Exception was thrown during database session. Rollback",
                    exc_info=ex,
                )
                await session.rollback()
                raise ex
