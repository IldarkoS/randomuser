import random
from typing import Optional, List, Protocol
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.user import User


class UserRepoProtocol(Protocol):
    async def add_users(self, users: List[User]) -> None:
        ...

    async def get_user(self, user_id: UUID) -> Optional[User]:
        ...

    async def get_random_user(self) -> Optional[User]:
        ...

    async def get_users_list(self, offset: int, limit: int) -> List[User]:
        ...

    async def count_users(self) -> int:
        ...


class UserRepoImpl(UserRepoProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_users(self, users: List[User]) -> None:
        self.session.add_all(users)
        await self.session.commit()

    async def get_user(self, user_id: UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return row

    async def get_random_user(self) -> Optional[User]:
        count = await self.count_users()
        if count == 0:
            return None
        random_offset = random.randint(0, count - 1)
        query = select(User).offset(random_offset).limit(1)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def count_users(self) -> int:
        query = select(func.count()).select_from(User)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_users_list(self, offset: int, limit: int) -> List[User]:
        query = select(User).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()