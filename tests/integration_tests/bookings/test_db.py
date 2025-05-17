from datetime import date
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0]

    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room.id,
        date_from=date(year=2025, month=4, day=15),
        date_to=date(year=2025, month=4, day=25),
        price=room.price
    )
    added_booking = await db.booking.add(booking_data)

    booking = await db.booking.get_one_or_none(**booking_data.model_dump())
    assert added_booking.id == booking.id

    update_data_booking = BookingAdd(
        user_id=user_id,
        room_id=room.id,
        date_from=date(year=2025, month=4, day=16),
        date_to=date(year=2025, month=4, day=22),
        price=500
    )
    await db.booking.edit(update_data_booking, id=booking.id)

    await db.booking.delete(id=booking.id)

    # await db.session.rollback()
    await db.commit()
