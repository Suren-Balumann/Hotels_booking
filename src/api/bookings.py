from fastapi import APIRouter
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import AllRoomsAreBookedException, \
    RoomNotFoundException, AllRoomsAreBookedHttpException, \
    RoomNotFoundHttpException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_user_bookings(user_id)


@router.post("")
async def reserve_room(user_id: UserIdDep, db: DBDep,
                       booking_data: BookingAddRequest):
    try:
        booking = await BookingService(db).reserve_room(booking_data, user_id)

    except RoomNotFoundException:
        raise RoomNotFoundHttpException()

    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHttpException()

    return {"status": "OK", "data": booking}
