from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from pydantic import BaseModel
from sqlalchemy import insert


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    # async def add(self, data: BaseModel):
    #
    #     query = insert(self.model).values(**data.model_dump()).returning(self.model)
    #     result = await self.session.execute(query)
    #     model = result.scalars().one_or_none()
    #     if model is None:
    #         return None
    #
    #     return self.schema.model_validate(model, from_attributes=True)
