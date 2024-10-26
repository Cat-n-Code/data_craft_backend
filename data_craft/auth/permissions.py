from abc import ABC, abstractmethod

from data_craft.users.models import User, Role


class BasePermission(ABC):
    @abstractmethod
    def has_permission(self, user: User | None) -> bool: ...


class Anonymous(BasePermission):
    def has_permission(self, user: User | None) -> bool:
        return user is None


class Authenticated(BasePermission):
    def has_permission(self, user: User | None) -> bool:
        return user is not None


class IsAdmin(BasePermission):
    def has_permission(self, user: User | None) -> bool:
        return user is not None and user.role == Role.admin

