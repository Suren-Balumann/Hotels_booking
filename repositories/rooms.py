from repositories.base import BaseRepository
from src.models.rooms import RoomOrm


class RoomRepository(BaseRepository):
    model = RoomOrm
