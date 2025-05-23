from fastapi import APIRouter, HTTPException, status
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.booking.get_all()


@router.get("/me")
async def my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.booking.get_filter_by(user_id=user_id)


@router.post("")
async def reserve_room(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Номер не найден"
        )
    hotel = await db.hotels.get_one(id=room.hotel_id)

    _booking_data = BookingAdd(
        **booking_data.model_dump(), price=room.price, user_id=user_id
    )
    try:
        booking = await db.booking.add_booking(
            _booking_data, hotel_id=hotel.id
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)

    await db.commit()
    return {"status": "OK", "data": booking}
