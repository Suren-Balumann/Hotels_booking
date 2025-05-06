from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.user import UserRepository
from src.repositories.booking import BookingRepository
from src.repositories.facilities import FacilitiesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UserRepository(self.session)
        self.booking = BookingRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
