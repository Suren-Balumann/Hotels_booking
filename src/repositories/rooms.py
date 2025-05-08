from datetime import date

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels
from sqlalchemy import select
from sqlalchemy.orm import selectinload


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

        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter(RoomOrm.id.in_(rooms_ids_to_get))
                 )

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        result = [RoomWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        return result

    async def get_room_by_id_rels(
            self,
            id: int
    ):
        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter_by(id=id)
                 )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None

        return RoomWithRels.model_validate(model, from_attributes=True)
