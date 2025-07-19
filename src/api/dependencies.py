from datetime import date

from fastapi import Depends, Query, HTTPException, status, Request
from pydantic import BaseModel
from typing import Annotated

from src.database import async_session_maker
from src.exceptions import (
    IncorrectTokenException,
    IncorrectTokenHttpException,
    ExpiredTokenException,
    ExpiredTokenHttpException,
)
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


async def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не предоставили токен доступа",
        )
    return token


async def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = await AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHttpException
    except ExpiredTokenException:
        raise ExpiredTokenHttpException

    user_id = data.get("user_id")
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


class FindDatesParams(BaseModel):
    date_from: Annotated[date, Query(example="2025-05-01")]
    date_to: Annotated[date, Query(example="2025-05-04")]


async def validate_dates(dates_params: FindDatesParams = Depends()) -> FindDatesParams:
    if dates_params.date_from >= dates_params.date_to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Дата заезда не может быть позже даты выезда",
        )

    else:
        return dates_params


DatesDep = Annotated[FindDatesParams, Depends(validate_dates)]
