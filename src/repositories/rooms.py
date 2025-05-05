from datetime import date

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room
from sqlalchemy import select, func
from src.models.bookings import BookingsOrm


class RoomsRepository(BaseRepository):
    model = RoomOrm
    schema = Room

    async def get_all_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filter_by(RoomOrm.id.in_(rooms_ids_to_get))
