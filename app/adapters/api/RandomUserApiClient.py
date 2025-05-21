from typing import List
from uuid import uuid4

import httpx

from app.config import settings
from app.models.domain.user import User
from app.ports.RandomUserApi import RandomUserApi


class RandomUserApiClient(RandomUserApi):
    BASE_URL = settings.RANDOM_USER_API_URL

    async def fetch_users(self, count: int) -> List[User]:
        async with httpx.AsyncClient() as client:
            params = {
                "results": count,
            }
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            return [self._parse_user(raw) for raw in data["results"]]

    def _parse_user(self, raw_response: dict) -> User:

        location = [
            raw_response["location"]["country"], raw_response["location"]["state"],
            raw_response["location"]["city"], raw_response["location"]["street"]["name"],
            str(raw_response["location"]["street"]["number"])
        ]

        return User(
            id=uuid4(),
            gender=raw_response["gender"],
            first_name=raw_response["name"]["first"],
            last_name=raw_response["name"]["last"],
            email=raw_response["email"],
            phone=raw_response["phone"],
            location=", ".join(location),
            photo_url=raw_response["picture"]["thumbnail"],
        )