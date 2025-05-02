from fastapi import APIRouter, Body, HTTPException, status
from src.schemas.rooms import RoomAdd, RoomPatch

from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(
        hotel_id: int,
        db: DBDep
):
    hotel = await db.hotels.get_by_id(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return await db.rooms.get_all(hotel_id=hotel_id)


@router.get('/room/{room_id}')
async def get_room_by_id(
        room_id: int,
        db: DBDep
):
    room = await db.rooms.get_by_id(id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return {"status": "OK", "data": room}


@router.post("/rooms")
async def create_room(
        db: DBDep,
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "Уютный",
                "value": {
                    "hotel_id": 10,
                    "title": "Уютный",
                    "description": "Уютный одноместный номер",
                    "price": 2000,
                    "quantity": 20,
                }
            },
            "2": {
                "summary": "Светлый",
                "value": {
                    "hotel_id": 17,
                    "title": "Светлый",
                    "description": "Светлый одноместный номер",
                    "price": 2500,
                    "quantity": 15,
                }
            },
            "3": {
                "summary": "Тёмный",
                "value": {
                    "hotel_id": 21,
                    "title": "Тёмный",
                    "description": "Тёмный одноместный номер",
                    "price": 2500,
                    "quantity": 15
                }
            },
            "4": {
                "summary": "Люкс",
                "value": {
                    "hotel_id": 25,
                    "title": "Люкс",
                    "description": "Люкс с видом на Море",
                    "price": 10000,
                    "quantity": 10
                }
            }
        })

):
    hotel = await db.hotels.get_by_id(id=room_data.hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    room = await db.rooms.add(room_data)

    await db.commit()

    return {"status": "OK", "data": room}


@router.put('/rooms/{room_id}')
async def change_room_all_values(
        db: DBDep,
        room_id: int,
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "Example",
                "value": {
                    "hotel_id": 10,
                    "title": "Example title",
                    "description": "Example description",
                    "price": 1234,
                    "quantity": 4321
                }
            }
        })
):
    room = await db.rooms.get_by_id(id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    await db.rooms.edit(data=room_data, id=room_id)

    await db.commit()

    return {"status": "OK"}


@router.patch('/rooms/{room_id}', summary="Частичное обновление даных комнаты")
async def change_room_value(
        db: DBDep,
        room_id: int,
        room_data: RoomPatch,
):
    await db.rooms.edit(data=room_data, exclude_unset=True, id=room_id)
    await db.commit()
    return {"message": "Successfully changed"}


@router.delete('/rooms/{room_id}')
async def delete_room(
        db: DBDep,
        room_id: int
):
    room = await db.rooms.get_one_or_none(id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status": "OK"}
