from unittest.mock import AsyncMock
from uuid import uuid4

from app.models.domain.user import User


class RandomUserApiMock(AsyncMock):
    def __init__(self):
        super().__init__()
        self.fetch_users = AsyncMock(side_effect=self._fake_users)

    @staticmethod
    async def _fake_users(count: int):
        return [
            User(
                id=uuid4(),
                gender="male",
                first_name=f"Test{i}",
                last_name=f"User",
                email=f"test{i}@example.com",
                phone='123456789',
                location='TestCiry',
                photo_url='photo_url',
            ) for i in range(count)
        ]