import pytest

from src.services.auth import AuthService


async def test_decode_and_encode_access_token():
    data = {"user_id": 12}
    jwt_token = await AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    decoded_token = await AuthService().decode_token(jwt_token)

    assert decoded_token
    assert decoded_token["user_id"] == data["user_id"]
