from datetime import date
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from data_craft.core.utils import NonEmptyStr


class Role(StrEnum):
    user = "USER"
    admin = "ADMIN"



class UserBaseSchema(BaseModel):
    email: EmailStr
    name: NonEmptyStr


class UserCreateSchema(UserBaseSchema):
    password: NonEmptyStr


class UserSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    role: Role = Role.user
    id: int


class UserUpdateSchema(BaseModel):
    email: EmailStr
    name: NonEmptyStr


class UserPasswordUpdateSchema(BaseModel):
    password: NonEmptyStr
