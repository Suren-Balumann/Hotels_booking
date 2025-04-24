from src.models.users import UserOrm
from src.repositories.base import BaseRepository
from src.schemas.users import User


class UserRepository(BaseRepository):
    model = UserOrm
    schema = User
