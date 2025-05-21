async def test_auth_flow(ac):
    response = await ac.post(url="/auth/register", json={
        "first_name": "Это второй",
        "last_name": "Test",
        "email": "SaintPiter@mail.ru",
        "password": "LongPassword12345"
    })

    assert response.status_code == 200
