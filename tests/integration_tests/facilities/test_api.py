async def test_add_facility(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Wi-Fi"
        }
    )
    answer = {
        "status": "OK",
        "data": {
            "id": isinstance(response.json()["data"]["id"], int),
            "title": "Wi-Fi"
        }
    }

    assert response.status_code == 200
    assert response.json() == answer
    assert isinstance(response.json(), dict)
    # print(f"{response.json()}")


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)



