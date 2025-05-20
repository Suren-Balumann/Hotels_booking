from datetime import date

from pydantic import BaseModel

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from sqlalchemy import select
from fastapi import HTTPException, status

from src.repositories.utils import is_there_free_rooms


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def add_booking(
            self,
            data: BaseModel
    ):
        query = is_there_free_rooms(room_id=data.room_id)
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        free_rooms_count = result.scalars().one_or_none()
        print(f"{free_rooms_count=}")

        if free_rooms_count == 0:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Все номера заняты")

        return await self.add(data)
