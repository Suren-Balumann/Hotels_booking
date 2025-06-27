from src.api.dependencies import DatesDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundException, RoomNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):

    async def get_all_by_time(self, dates: DatesDep, hotel_id: int):
        return await self.db.rooms.get_all_by_time(
            hotel_id=hotel_id, date_from=dates.date_from, date_to=dates.date_to
        )

    async def get_room(self, room_id: int):
        return await self.db.rooms.get_room_by_id_rels(id=room_id)

    async def create_room(
            self,
            hotel_id: int,
            room_data: RoomAddRequest
    ):

        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(data=rooms_facilities_data)

        await self.db.commit()
        return room

    async def edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomAddRequest,
    ):
        await HotelService(self.db).get_hotel_check(hotel_id=hotel_id)

        await self.get_room_with_rels_check(room_id=room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        await self.db.rooms.edit(data=_room_data, id=room_id)

        await self.db.rooms_facilities.add_rooms_facilities(
            room_id=room_id, facility_ids=room_data.facilities_ids
        )

        await self.db.commit()

    async def partially_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_check(hotel_id=hotel_id)

        await self.get_room_with_rels_check(room_id=room_id)

        _room_data = RoomPatch(**room_data.model_dump())
        await self.db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
        await self.db.rooms_facilities.add_rooms_facilities(
            room_id=room_id, facility_ids=room_data.facilities_ids
        )

        await self.db.commit()

    async def delete_room(self, room_id: int):
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        await self.db.rooms.delete(id=room_id)

        await self.db.commit()

    async def get_room_with_rels_check(self, room_id: int):
        try:
            await self.db.rooms.get_room_by_id_rels(id=room_id)

        except ObjectNotFoundException:
            raise RoomNotFoundException
