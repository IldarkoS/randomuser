from typing import List, Optional
from uuid import UUID

from app.adapters.api.RandomUserApiClient import RandomUserApiClient
from app.adapters.db.UserRepoPostgres import UserRepoPostgres
from app.models.domain.user import User


class UserService:
    def __init__(self, user_repo: UserRepoPostgres, user_api: RandomUserApiClient):
        self.user_repo = user_repo
        self.user_api = user_api

    async def load_users(self, count: int) -> None:
        users = await self.user_api.fetch_users(count=count)
        await self.user_repo.add_users(users)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return await self.user_repo.get_user(user_id)

    async def get_random_user(self) -> Optional[User]:
        return await self.user_repo.get_random_user()

    async def get_users_list(self, page: int, size: int) -> List[User]:
        offset = (page - 1) * size
        return await self.user_repo.get_users_list(offset=offset, limit=size)

    async def count_users(self) -> int:
        return await self.user_repo.count_users()