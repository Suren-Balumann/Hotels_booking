import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.rooms import RoomOrm


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomOrm"]] = relationship(
        back_populates="facilities", secondary="rooms_facilities"
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
