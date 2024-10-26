

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from data_craft.core.db_manager import Base
from data_craft.core.utils import NonEmptyStr
from data_craft.users.schemas import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[NonEmptyStr] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(
         nullable=False
    )


    __table_args__ = (UniqueConstraint(email),)
