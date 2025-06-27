from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):

    async def get_filtered_by_time(
            self,
            pagination,
            dates,
            title: str | None,
            location: str | None,
    ):
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
            date_from=dates.date_from,
            date_to=dates.date_to,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(
            self,
            hotel_id: int,
            hotel_data: HotelAdd
    ):
        await self.db.hotels.edit(data=hotel_data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_data: HotelPatch, hotel_id: int):
        await self.db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_check(self, hotel_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
