from pydantic import BaseModel, EmailStr

from data_craft.core.utils import NonEmptyStr


class LoginCredentials(BaseModel):
    email: EmailStr
    password: NonEmptyStr


class AuthTokenSchema(BaseModel):
    token: str


class AuthTokenPayload(BaseModel):
    user_id: int
