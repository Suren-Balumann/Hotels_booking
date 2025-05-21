# from datetime import date
# from src.schemas.bookings import BookingAdd
#
#
# async def test_booking_crud(db):
#     user_id = (await db.users.get_all())[0].id
#     room = (await db.rooms.get_all())[0]
#
#     booking_data = BookingAdd(
#         user_id=user_id,
#         room_id=room.id,
#         date_from=date(year=2025, month=4, day=15),
#         date_to=date(year=2025, month=4, day=25),
#         price=room.price
#     )
#     added_booking = await db.booking.add(booking_data)
#
#     booking = await db.booking.get_one_or_none(**booking_data.model_dump())
#     assert booking
#     assert added_booking.id == booking.id
#     assert booking.room_id == booking_data.room_id
#     assert booking.user_id == booking_data.user_id
#
#     updated_date = date(year=2025, month=4, day=22)
#     new_price = 500
#     update_data_booking = BookingAdd(
#         user_id=user_id,
#         room_id=room.id,
#         date_from=date(year=2025, month=4, day=16),
#         date_to=updated_date,
#         price=new_price
#     )
#
#     await db.booking.edit(update_data_booking, id=booking.id)
#     updated_booking = await db.booking.get_one_or_none(id=added_booking.id)
#     assert updated_booking
#     assert updated_booking.id == added_booking.id
#     assert updated_booking.date_to == updated_date
#     assert updated_booking.price == new_price
#
#     await db.booking.delete(id=booking.id)
#     deleted_booking = await db.booking.get_one_or_none(id=added_booking.id)
#     assert not deleted_booking
#
#     # await db.session.rollback()
#     await db.commit()
