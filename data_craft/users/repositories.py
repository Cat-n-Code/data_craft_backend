from sqlalchemy import and_, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from data_craft.core.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from data_craft.users.models import User


class UserRepository:
    async def get_by_id(self, session: AsyncSession, id: int):
        # return await session.get(User, id)
        statement = (
            select(User)
            .where(User.id == id)
        )

        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def exists_by_email(self, session: AsyncSession, email: str):
        statement = select(exists().where(User.email == email))
        result = await session.execute(statement)
        return result.scalar_one()

    async def get_all(self, session: AsyncSession, page: int, size: int):
        statement = select(User).order_by(User.id).offset(page * size).limit(size)
        result = await session.execute(statement)
        return result.scalars().all()

    async def count_all(self, session: AsyncSession):
        statement = select(func.count()).select_from(User)
        result = await session.execute(statement)
        return result.scalar_one()


    async def save(self, session: AsyncSession, user: User):
        session.add(user)
        await session.flush()
        await session.commit()
        return user

    async def delete(self, session: AsyncSession, user: User):
        await session.delete(user)
        await session.commit()
        return user
