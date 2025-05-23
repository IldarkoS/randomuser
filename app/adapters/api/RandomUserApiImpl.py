from typing import List, Protocol
from uuid import uuid4

import httpx
from loguru import logger

from app.config import settings
from app.models.domain.user import User


class RandomUserApiProtocol(Protocol):
    async def fetch_users(self, count: int) -> List[User]:
        ...

class RandomUserApiImpl(RandomUserApiProtocol):
    def __init__(self):
        self.BASE_URL = settings.RANDOM_USER_API_URL

    async def fetch_users(self, count: int) -> List[User]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                params = {"results": count}
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()

                data = response.json()
                return [self._parse_user(raw) for raw in data["results"]]

        except httpx.RequestError as e:
            logger.error(f"Ошибка запроса к {self.BASE_URL}: {e}")
            raise RuntimeError("Ошибка соединения с внешним API randomuser.me") from e

        except httpx.HTTPStatusError as e:
            logger.error(f"API вернул ошибку {e.response.status_code}: {e.response.text}")
            raise RuntimeError("Ошибка при получении данных от API randomuser.me") from e

        except Exception as e:
            logger.exception("Непредвиденная ошибка при получении пользователей")
            raise RuntimeError("Не удалось загрузить пользователей") from e

    @staticmethod
    def _parse_user(raw_response: dict) -> User:

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