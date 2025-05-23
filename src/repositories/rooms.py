from datetime import date

from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomOrm
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class RoomsRepository(BaseRepository):
    model = RoomOrm
    mapper = RoomDataMapper

    async def get_all_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomOrm.id.in_(rooms_ids_to_get))
        )

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        result = [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]
        return result

    async def get_room_by_id_rels(self, id: int):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(id=id)
        )
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        return RoomWithRels.model_validate(model, from_attributes=True)
