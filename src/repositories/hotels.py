from sqlalchemy import select
from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelOrm


class HotelsRepository(BaseRepository):
    model = HotelOrm
    schema = Hotel

    async def get_all(self, title, location, limit, offset):

        query = select(self.model)

        if title:
            query = query.filter(self.model.title.ilike(f'%{title}%'))

        if location:
            query = query.filter(HotelOrm.location.ilike(f'%{location}%'))

        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        result = [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
        return result

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        result = [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
        return result
