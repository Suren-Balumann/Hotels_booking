from fastapi import APIRouter, Body, HTTPException, status, Query

from src.exceptions import ObjectNotFoundException, FoKeyObjectCannotBeDeleted
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

from src.api.dependencies import DBDep, DatesDep
from datetime import date

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(
        hotel_id: int,
        db: DBDep,
        dates: DatesDep
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отеля не существует"
        )
    return await db.rooms.get_all_by_time(
        hotel_id=hotel_id, date_from=dates.date_from, date_to=dates.date_to
    )


@router.get("/room/{room_id}")
async def get_room_by_id(room_id: int, db: DBDep):
    try:
        room = await db.rooms.get_room_by_id_rels(id=room_id)

    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Номера не существует")

    return {"status": "OK", "data": room}


@router.post("/rooms")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": {
                    "summary": "Уютный",
                    "value": {
                        # "hotel_id": 10,
                        "title": "Уютный",
                        "description": "Уютный одноместный номер",
                        "price": 2000,
                        "quantity": 20,
                        "facilities_ids": [2, 3, 4],
                    },
                },
                "2": {
                    "summary": "Светлый",
                    "value": {
                        # "hotel_id": 17,
                        "title": "Светлый",
                        "description": "Светлый одноместный номер",
                        "price": 2500,
                        "quantity": 15,
                        "facilities_ids": [3],
                    },
                },
                "3": {
                    "summary": "Тёмный",
                    "value": {
                        # "hotel_id": 21,
                        "title": "Тёмный",
                        "description": "Тёмный одноместный номер",
                        "price": 2500,
                        "quantity": 15,
                        "facilities_ids": [4],
                    },
                },
                "4": {
                    "summary": "Люкс",
                    "value": {
                        # "hotel_id": 25,
                        "title": "Люкс",
                        "description": "Люкс с видом на Море",
                        "price": 10000,
                        "quantity": 10,
                        "facilities_ids": [2],
                    },
                },
            }
        ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отеля не существует"
        )
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(data=rooms_facilities_data)

    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room_all_values(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": {
                    "summary": "Example",
                    "value": {
                        # "hotel_id": 10,
                        "title": "Example title",
                        "description": "Example description",
                        "price": 1234,
                        "quantity": 4321,
                        "facilities_ids": [3, 4],
                    },
                }
            }
        ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отеля не существует"
        )

    try:
        await db.rooms.get_room_by_id_rels(id=room_id)

    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Номера не существует")

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.edit(data=_room_data, id=room_id)

    await db.rooms_facilities.add_rooms_facilities(
        room_id=room_id, facility_ids=room_data.facilities_ids
    )

    await db.commit()

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
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отеля не существует"
        )
    try:
        await db.rooms.get_room_by_id_rels(id=room_id)

    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Номера не существует")

    _room_data = RoomPatch(**room_data.model_dump())
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
    await db.rooms_facilities.add_rooms_facilities(
        room_id=room_id, facility_ids=room_data.facilities_ids
    )

    await db.commit()
    return {"message": "Successfully changed"}


@router.delete("/rooms/{room_id}")
async def delete_room(db: DBDep, room_id: int):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Номера не существует"
        )
    try:
        await db.rooms.delete(id=room_id)
    except FoKeyObjectCannotBeDeleted:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="Необхадимо удалить связующие данные")
    await db.commit()
    return {"status": "OK"}
