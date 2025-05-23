from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.api.RandomUserApiImpl import RandomUserApiProtocol, RandomUserApiImpl
from app.adapters.db.UserRepoImpl import UserRepoProtocol, UserRepoImpl
from app.core.db import get_async_session
from app.services.user_service import UserServiceImpl, UserServiceProtocol

Session = Annotated[AsyncSession, Depends(get_async_session)]

def get_users_repo(session: Session) -> UserRepoProtocol:
    return UserRepoImpl(session=session)

UserRepo = Annotated[UserRepoProtocol, Depends(get_users_repo)]


def get_users_random_api() -> RandomUserApiProtocol:
    return RandomUserApiImpl()

RandomUserApi = Annotated[RandomUserApiProtocol, Depends(get_users_random_api)]


def get_users_use_case(user_repo: UserRepo, random_user_api: RandomUserApi) -> UserServiceProtocol:
    return UserServiceImpl(user_repo=user_repo, user_api=random_user_api)

UserUseCase = Annotated[UserServiceProtocol, Depends(get_users_use_case)]