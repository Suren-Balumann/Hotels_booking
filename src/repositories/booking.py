from datetime import date

from src.exceptions import AllRoomsAreBookedException
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from sqlalchemy import select
from fastapi import HTTPException, status

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=data.date_from, date_to=data.date_to
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            # print(f"{data=}")
            new_booking = await self.add(data)
            return new_booking
        else:
            raise AllRoomsAreBookedException
