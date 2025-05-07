from sqlalchemy import select, insert

# from sqlalchemy.dialects.postgresql import insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def get_facilities_ids(self, **filter_by):
        query = (select(self.model.facility_id)
                 .select_from(self.model)
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        result = result.scalars().all()
        return result

    async def add_rooms_facilities(
            self,
            room_id: int,
            facility_ids: list[int] | None = None
    ):
        if facility_ids:
            exists_room_f_ids = await self.get_facilities_ids(room_id=room_id)
            if exists_room_f_ids:
                [await self.delete(room_id=room_id, facility_id=f_id) for f_id in exists_room_f_ids if
                 f_id not in facility_ids]

            add_facilities = [RoomFacilityAdd(
                room_id=room_id,
                facility_id=f_id
            ) for f_id in facility_ids if f_id not in exists_room_f_ids]

            if add_facilities:
                await self.add_bulk(data=add_facilities)
