import pytest
import json
from httpx import AsyncClient, ASGITransport
from src.config import settings
from src.database import engine_null_pool, Base
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_mocks_hotels_and_rooms(setup_database):
    with open("tests/mock_hotels.json", "r") as file:
        hotels = [HotelAdd(**hotel) for hotel in json.load(file)]

    with open("tests/mock_rooms.json", "r") as file:
        rooms = [RoomAdd(**room) for room in json.load(file)]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        [await db.hotels.add(hotel) for hotel in hotels]
        [await db.rooms.add(room) for room in rooms]
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def add_user(add_mocks_hotels_and_rooms):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(url="/auth/register", json={
            "first_name": "Тестовый",
            "last_name": "Тестовый",
            "email": "Testoviy@mail.ru",
            "password": "LongPassword12345"
        })
