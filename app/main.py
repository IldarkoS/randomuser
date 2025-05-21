from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.delivery.views import users as user_views
from app.services.user_service import UserService


def get_user_service() -> UserService:
    from app.adapters.db.UserRepoPostgres import UserRepoPostgres
    from app.adapters.api.RandomUserApiClient import RandomUserApiClient
    from app.adapters.db.database import async_session
    return UserService(
        UserRepoPostgres(async_session),
        RandomUserApiClient(),
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    user_service = get_user_service()
    await user_service.load_users(1000)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_views.router, tags=["users"])