from datetime import date
from sqlalchemy import select

from src.models.rooms import RoomOrm
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking

from src.repositories.base import BaseRepository
from src.models.hotels import HotelOrm


class HotelsRepository(BaseRepository):
    model = HotelOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        title: str,
        location: str,
        limit: int,
        offset: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomOrm.hotel_id)
            .select_from(RoomOrm)
            .filter(RoomOrm.id.in_(rooms_ids_to_get))
        )
        # print(hotels_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = select(self.model).filter(HotelOrm.id.in_(hotels_ids_to_get))

        if title:
            query = query.filter(self.model.title.ilike(f"%{title}%"))

        if location:
            query = query.filter(HotelOrm.location.ilike(f"%{location}%"))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        result = [
            self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()
        ]
        return result

