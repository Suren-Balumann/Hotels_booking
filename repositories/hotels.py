from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.hotels import HotelOrm


class HotelsRepository(BaseRepository):
    model = HotelOrm

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

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()
