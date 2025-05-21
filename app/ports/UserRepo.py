from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.models.domain.user import User


class UserRepo(ABC):
    @abstractmethod
    async def add_users(self, users: List[User]) -> None:
        ...

    @abstractmethod
    async def get_user(self, user_id: UUID) -> Optional[User]:
        ...

    @abstractmethod
    async def get_random_user(self) -> Optional[User]:
        ...

    @abstractmethod
    async def get_users_list(self, offset: int, limit: int) -> List[User]:
        ...

    @abstractmethod
    async def count_users(self) -> int:
        ...