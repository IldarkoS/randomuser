from typing import List, Optional
from uuid import UUID

from loguru import logger

from app.adapters.api.RandomUserApiClient import RandomUserApiClient
from app.adapters.db.UserRepoPostgres import UserRepoPostgres
from app.models.domain.user import User


class UserService:
    def __init__(self, user_repo: UserRepoPostgres, user_api: RandomUserApiClient):
        self.user_repo = user_repo
        self.user_api = user_api

    async def load_users(self, count: int) -> None:
        users = await self.user_api.fetch_users(count=count)
        logger.info(f"Loaded {count} users!")
        await self.user_repo.add_users(users)
        logger.info(f"Saved {count} users!")

    async def get_user(self, user_id: UUID) -> Optional[User]:
        result = await self.user_repo.get_user(user_id)
        logger.info(f"Received user with ID: {user_id} !")
        return result

    async def get_random_user(self) -> Optional[User]:
        result = await self.user_repo.get_random_user()
        logger.info(f"Received random user with ID: {result.id} !")
        return result

    async def get_users_list(self, page: int, size: int) -> List[User]:
        offset = (page - 1) * size
        result = await self.user_repo.get_users_list(offset=offset, limit=size)
        logger.info(f"Received users list!")
        return result

    async def count_users(self) -> int:
        return await self.user_repo.count_users()