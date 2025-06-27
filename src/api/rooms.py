from fastapi import APIRouter, Body, HTTPException, status

from src.api.examples.rooms import post_example, put_example
from src.exceptions import ObjectNotFoundException, HotelNotFoundHttpException, \
    RoomNotFoundHttpException, HotelNotFoundException, RoomNotFoundException

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest

from src.api.dependencies import DBDep, DatesDep
from src.services.hotels import HotelService
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, db: DBDep, dates: DatesDep):
    try:
        await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHttpException
    return await RoomService(db).get_all_by_time(dates, hotel_id)


@router.get("/room/{room_id}")
async def get_room_by_id(room_id: int, db: DBDep):
    try:
        room = await RoomService(db).get_room(room_id)

    except ObjectNotFoundException:
        raise RoomNotFoundHttpException

    return {"status": "OK", "data": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples=post_example
        ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)

    except HotelNotFoundException:
        raise HotelNotFoundHttpException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room_all_values(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples=put_example
        ),
):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)

    except HotelNotFoundException:
        raise HotelNotFoundHttpException
    except RoomNotFoundException:
        raise RoomNotFoundHttpException

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное обновление даных комнаты"
)
async def change_room_value(
        hotel_id: int,
        db: DBDep,
        room_id: int,
        room_data: RoomPatchRequest,
):
    try:
        await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)

    except HotelNotFoundException:
        raise HotelNotFoundHttpException
    except RoomNotFoundException:
        raise RoomNotFoundHttpException

    return {"message": "Successfully changed"}


@router.delete("/rooms/{room_id}")
async def delete_room(db: DBDep, room_id: int):
    try:
        await RoomService(db).delete_room(room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHttpException
    return {"status": "OK"}
