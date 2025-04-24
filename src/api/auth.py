from fastapi import APIRouter, Body, HTTPException, status
from passlib.context import CryptContext

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.user import UserRepository
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd = Body(openapi_examples={
            "1": {
                "summary": "Алексей",
                "value": {
                    "first_name": "Алексей",
                    "last_name": "Дементьев",
                    "email": "alex123@mail.ru",
                    "password": "LongPassword12345"
                }
            },
            "2": {
                "summary": "Владимир",
                "value": {
                    "first_name": "Владимир",
                    "last_name": "Колесников",
                    "email": "vlad_kol@mail.ru",
                    "password": "ShortPassword12345"
                }
            }

        })
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hashed_password
    )
    try:
        async with async_session_maker() as session:
            await UserRepository(session).add(new_user_data)
            await session.commit()

            return {"status": "OK"}

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Already exists")
