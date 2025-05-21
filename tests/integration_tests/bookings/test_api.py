import pytest


@pytest.mark.parametrize("hotel_id,room_id,date_from,date_to,status_code", [
    (1, 1, "2025-05-01", "2025-05-08", 200),
    (1, 1, "2025-05-01", "2025-05-08", 200),
    (1, 1, "2025-05-01", "2025-05-08", 200),
    (1, 1, "2025-05-01", "2025-05-08", 200),
    (1, 1, "2025-05-01", "2025-05-08", 200),
    (1, 1, "2025-05-01", "2025-05-08", 406),
])
async def test_add_booking(
        hotel_id,
        room_id,
        date_from,
        date_to,
        status_code,
        db,
        authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="function")
async def delete_all_bookings(db):
    await db.booking.delete_all_entries()
    await db.commit()


@pytest.mark.parametrize("hotel_id,room_id,date_from,date_to,status_code,records", [
    (1, 1, "2025-05-01", "2025-05-08", 200, 1),
    (1, 1, "2025-05-01", "2025-05-08", 200, 2),
    (1, 1, "2025-05-01", "2025-05-08", 200, 3)
])
async def test_add_and_get_bookings(
        hotel_id,
        room_id,
        date_from,
        date_to,
        status_code,
        records,
        delete_all_bookings,
        authenticated_ac
):
    for _ in range(records):
        response = await authenticated_ac.post(
            "/bookings",
            json={
                "hotel_id": hotel_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to
            }
        )
        assert response.status_code == status_code

    response = await authenticated_ac.get(
        "/bookings/me"
    )
    if response.status_code == 200:
        assert len(response.json()) == records
