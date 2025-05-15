from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelOrm
from src.models.rooms import RoomOrm
from src.models.users import UserOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelOrm
    schema = Hotel


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User


class RoomDataMapper(DataMapper):
    db_model = RoomOrm
    schema = Room


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
