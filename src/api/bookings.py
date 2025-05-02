from fastapi import APIRouter, HTTPException, status
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/booking", tags=["Бронирование"])


@router.post("")
async def reserve_room(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest

):
    room = await db.rooms.get_by_id(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    booking_data = BookingAdd(**booking_data.model_dump(), price=room.price, user_id=user_id)

    await db.booking.add(booking_data)
    await db.commit()
    return {"status": "OK"}
