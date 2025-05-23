import pytest


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "model",
    [
        (
            {
                "first_name": "Это второй",
                "last_name": "Test",
                "email": "SaintPiter@mail.ru",
                "password": "LongPassword12345",
            }
        ),
        (
            {
                "first_name": "Это второй",
                "last_name": "Test",
                "email": "SaintPiter@mail.ru",
                "password": "LongPassword12345",
            }
        ),
        (
            {
                "first_name": "Это второй",
                "last_name": "Test",
                "email": "SaintPiter@mail.ru",
                "password": "WrongPassword12345",
            }
        ),
    ],
)
async def test_auth_flow(model, ac):
    response = await ac.post(url="/auth/register", json=model)

    if response.status_code == 200:
        assert response.json() == {"status": "OK"}

    if response.status_code == 405:
        assert response.json() == {"detail": "Already exists"}

    response = await ac.post("/auth/login", json=model)
    if response.status_code == 200:
        assert "access_token" in ac.cookies

    if response.status_code == 401:
        assert response.json() == {"detail": "Неверный пароль"}

    response = await ac.get("/auth/me")
    if response.status_code == 200:
        assert response.json()["first_name"] == model["first_name"]
        assert response.json()["last_name"] == model["last_name"]
        assert response.json()["email"] == model["email"]
    else:
        assert response.status_code == 401

    response = await ac.post("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in ac.cookies

    response = await ac.get("/auth/me")
    assert response.status_code == 401
