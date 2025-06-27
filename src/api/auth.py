from fastapi import APIRouter, Body, HTTPException, status, Response

from src.api.dependencies import UserIdDep, DBDep
from src.api.examples.auth import register_example, login_example
from src.exceptions import ObjectAlreadyExistsException, \
    UserAlreadyExistsException, UserAlreadyExistsHttpException, \
    UserDoesNotRegisteredException, WrongPasswordException, \
    UserDoesNotRegisteredHttpException, WrongPasswordHttpException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        db: DBDep,
        data: UserRequestAdd = Body(
            openapi_examples=register_example
        ),
):
    try:
        return await AuthService(db).register_user(data)

    except UserAlreadyExistsException:
        raise UserAlreadyExistsHttpException()


@router.post("/login")
async def login_user(
        response: Response,
        db: DBDep,
        data: UserRequestAdd = Body(
            openapi_examples=login_example
        ),
):
    try:
        access_token = await AuthService(db).login_user(data)

    except UserDoesNotRegisteredException:
        raise UserDoesNotRegisteredHttpException()

    except WrongPasswordException:
        raise WrongPasswordHttpException()

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def only_auth(user_id: UserIdDep, db: DBDep):
    try:
        return await AuthService(db).get_user(user_id)

    except UserDoesNotRegisteredException:
        raise UserDoesNotRegisteredHttpException()


@router.post("/logout")
async def logout_system(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
