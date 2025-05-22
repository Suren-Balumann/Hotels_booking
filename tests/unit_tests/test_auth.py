import pytest

from src.services.auth import AuthService


async def test_create_access_token():
    data = {"user_id": 12}
    jwt_token = await AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)
