from pydantic import BaseModel
from datetime import date


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingAddRequest):
    price: int
    user_id: int


class Booking(BookingAdd):
    id: int
