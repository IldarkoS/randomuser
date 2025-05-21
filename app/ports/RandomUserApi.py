from abc import ABC, abstractmethod
from typing import List

from app.models.domain.user import User


class RandomUserApi(ABC):
    @abstractmethod
    async def fetch_users(self, count: int) -> List[User]:
        ...