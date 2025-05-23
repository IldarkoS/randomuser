from typing import List, Optional, Protocol, Self
from uuid import UUID

from loguru import logger

from app.adapters.api.RandomUserApiImpl import RandomUserApiProtocol
from app.adapters.db.UserRepoImpl import UserRepoProtocol
from app.schemas import UserSchema


class UserServiceProtocol(Protocol):
    async def load_users(self: Self, count: int) -> None:
        ...

    async def get_user(self: Self, user_id: UUID) -> UserSchema:
        ...

    async def get_random_user(self: Self) -> Optional[UserSchema]:
        ...

    async def get_users_list(self: Self, page: int, size: int) -> List[UserSchema]:
        ...


class UserServiceImpl(UserServiceProtocol):
    def __init__(self, user_repo: UserRepoProtocol, user_api: RandomUserApiProtocol) -> None:
        self.user_repo = user_repo
        self.user_api = user_api

    async def load_users(self, count: int) -> None:
        users = await self.user_api.fetch_users(count=count)
        logger.info(f"Loaded {count} users!")
        await self.user_repo.add_users(users)
        logger.info(f"Saved {count} users!")

    async def get_user(self, user_id: UUID) -> Optional[UserSchema]:
        result = await self.user_repo.get_user(user_id)
        logger.info(f"Received user with ID: {user_id} !")
        return UserSchema.model_validate(result, from_attributes=True)

    async def get_random_user(self) -> Optional[UserSchema]:
        result = await self.user_repo.get_random_user()
        logger.info(f"Received random user with ID: {result.id} !")
        return UserSchema.model_validate(result, from_attributes=True)

    async def get_users_list(self, page: int, size: int) -> List[UserSchema]:
        offset = (page - 1) * size
        result = await self.user_repo.get_users_list(offset=offset, limit=size)
        logger.info(f"Received users list!")
        return [UserSchema.model_validate(user, from_attributes=True) for user in result]

    async def count_users(self) -> int:
        return await self.user_repo.count_users()