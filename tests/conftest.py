import pytest
import json
from httpx import AsyncClient, ASGITransport
from unittest import mock

# def mocked_cache(*args, **kwargs):
#     def wrapper(func):
#         return func
#
#     return wrapper

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.dependencies import get_db
from src.config import settings
from src.database import engine_null_pool, Base
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def get_db_nool_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        # print("Я ПЕРЕЗАПИСАН")
        yield db


app.dependency_overrides[get_db] = get_db_nool_pool


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_nool_pool():
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file:
        hotels = [HotelAdd.model_validate(hotel) for hotel in json.load(file)]

    with open("tests/mock_rooms.json", encoding="utf-8") as file:
        rooms = [RoomAdd.model_validate(room) for room in json.load(file)]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def add_user(ac, setup_database):
    await ac.post(url="/auth/register", json={
        "first_name": "Тестовый",
        "last_name": "Тестовый",
        "email": "Testoviy@mail.ru",
        "password": "LongPassword12345"
    })


@pytest.fixture(scope="session")
async def authenticated_ac(ac, add_user):
    await ac.post(
        "/auth/login",
        json={
            "first_name": "Тестовый",
            "last_name": "Тестовый",
            "email": "Testoviy@mail.ru",
            "password": "LongPassword12345"
        }
    )
    assert "access_token" in ac.cookies
    yield ac
