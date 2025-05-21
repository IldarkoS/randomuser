import random
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func

from app.adapters.db.database import async_session
from app.models.domain.user import User
from app.ports.UserRepo import UserRepo


class UserRepoPostgres(UserRepo):
    def __init__(self, session_factory=async_session):
        self._session_factory = session_factory

    async def add_users(self, users: List[User]) -> None:
        async with self._session_factory() as session:
            session.add_all(users)
            await session.commit()

    async def get_user(self, user_id: UUID) -> Optional[User]:
        async with self._session_factory() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            row = result.scalar_one_or_none()
            return row

    async def get_random_user(self) -> Optional[User]:
        async with self._session_factory() as session:
            count = await self.count_users()
            if count == 0:
                return None
            random_offset = random.randint(0, count - 1)
            query = select(User).offset(random_offset).limit(1)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def count_users(self) -> int:
        async with self._session_factory() as session:
            query = select(func.count()).select_from(User)
            result = await session.execute(query)
            return result.scalar_one()

    async def get_users_list(self, offset: int, limit: int) -> List[User]:
        async with self._session_factory() as session:
            query = select(User).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()