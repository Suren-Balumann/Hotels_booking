from src.exceptions import (
    ObjectNotFoundException,
    AllRoomsAreBookedException,
    RoomNotFoundException,
)
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.booking.get_all()

    async def get_user_bookings(self, user_id: int):
        return await self.db.booking.get_filter_by(user_id=user_id)

    async def reserve_room(self, booking_data: BookingAddRequest, user_id: int):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        hotel = await self.db.hotels.get_one(id=room.hotel_id)

        _booking_data = BookingAdd(
            **booking_data.model_dump(), price=room.price, user_id=user_id
        )
        try:
            booking = await self.db.booking.add_booking(
                _booking_data, hotel_id=hotel.id
            )
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedException

        await self.db.commit()
        return booking
