from src.repositories.base import BaseRepository
from src.models.rooms import RoomOrm
from src.schemas.rooms import Room
from sqlalchemy import select


class RoomsRepository(BaseRepository):
    model = RoomOrm
    schema = Room

    async def get_all(self, hotel_id: int):
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        result = [self.schema.model_validate(room, from_attributes=True) for room in result.scalars().all()]
        return result
