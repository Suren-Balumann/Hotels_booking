from fastapi import APIRouter, Body, HTTPException, status, Response

from src.api.dependencies import UserIdDep
from src.exceptions import ObjectAlreadyExists
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.user import UserRepository
from sqlalchemy.exc import IntegrityError
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Алексей",
                    "value": {
                        "first_name": "Алексей",
                        "last_name": "Дементьев",
                        "email": "alex123@mail.ru",
                        "password": "LongPassword12345",
                    },
                },
                "2": {
                    "summary": "Владимир",
                    "value": {
                        "first_name": "Владимир",
                        "last_name": "Колесников",
                        "email": "vlad_kol@mail.ru",
                        "password": "ShortPassword12345",
                    },
                },
            }
        ),
):
    hashed_password = await AuthService().hash_password(password=data.password)
    new_user_data = UserAdd(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hashed_password,
    )
    try:
        async with async_session_maker() as session:
            await UserRepository(session).add(new_user_data)
            await session.commit()

            return {"status": "OK"}

    except ObjectAlreadyExists as ex:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=ex.detail
        )


@router.post("/login")
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Алексей",
                    "value": {
                        "first_name": "Алексей",
                        "last_name": "Дементьев",
                        "email": "alex123@mail.ru",
                        "password": "LongPassword12345",
                    },
                },
                "2": {
                    "summary": "Владимир",
                    "value": {
                        "first_name": "Владимир",
                        "last_name": "Колесников",
                        "email": "vlad_kol@mail.ru",
                        "password": "ShortPassword12345",
                    },
                },
            }
        ),
):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_user_with_hashed_password(
            email=data.email
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь с таким email не зарегестрирован",
            )
        if not await AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
            )
        access_token = await AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me")
async def only_auth(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout_system(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
