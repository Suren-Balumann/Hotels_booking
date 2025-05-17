from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(
        title="Отель 5 звезд у моря",
        location="Сочи, ул.Моря, 1",
    )
    await db.hotels.add(hotel_data)
    await db.commit()
