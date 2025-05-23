from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.config import settings
from app.core.db import async_session
from app.core.logger import init_logger
from app.delivery.views import users as user_views
from app.depends import get_users_repo, get_users_random_api, get_users_use_case


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    logger.info(f"Application started!")
    async with async_session() as session:
        user_repo = get_users_repo(session=session)
    random_user_api = get_users_random_api()
    user_use_case = get_users_use_case(user_repo, random_user_api)
    await user_use_case.load_users(settings.USERS_ON_START)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_views.router, tags=["users"])