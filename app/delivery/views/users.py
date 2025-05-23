import math
from uuid import UUID

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from app.config import settings
from app.delivery.dto.user_dto import UserDTO
from app.depends import UserUseCase

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, user_use_case: UserUseCase, page: int = 1):
    users = await user_use_case.get_users_list(page=page, size=settings.PAGE_LIMIT)
    total = await user_use_case.count_users()

    total_pages = math.ceil(total / settings.PAGE_LIMIT)
    message = request.cookies.get("load_message")

    if total_pages <= 7:
        visible_pages = list(range(1, total_pages + 1))
    else:
        visible_pages = [1, 2, 3, "...", total_pages - 1, total_pages]

    return templates.TemplateResponse("users/index.html", {
        "request": request,
        "users": [UserDTO.model_validate(user, from_attributes=True) for user in users],
        "page": page,
        "pages": (total // settings.PAGE_LIMIT) + 1,
        "visible_pages": visible_pages,
        "load_message": message
    })


@router.get("/user/{user_id}", response_class=HTMLResponse)
async def user_detail(request: Request, user_id: str, user_use_case: UserUseCase):
    user = await user_use_case.get_user(UUID(user_id))
    return templates.TemplateResponse("users/detail.html", {
        "request": request,
        "user": UserDTO.model_validate(user, from_attributes=True),
    })


@router.get("/random", response_class=HTMLResponse)
async def random_user(request: Request, user_use_case: UserUseCase):
    user = await user_use_case.get_random_user()
    return templates.TemplateResponse("users/detail.html", {
        "request": request,
        "user": UserDTO.model_validate(user, from_attributes=True),
    })

@router.post("/load")
async def load_users(user_use_case: UserUseCase, count: int = Form(...)):
    await user_use_case.load_users(count)
    response = RedirectResponse("/", status_code=HTTP_302_FOUND)
    response.set_cookie("load_message", f"Loaded {count} user(s)!", max_age=2)
    return response