from fastapi import APIRouter, HTTPException, status
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


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

    booking = await db.booking.add(booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_all_bookings(
        db: DBDep
):
    return await db.booking.get_all()


@router.get('/me')
async def my_bookings(
        user_id: UserIdDep,
        db: DBDep
):
    return await db.booking.get_filter_by(user_id=user_id)
