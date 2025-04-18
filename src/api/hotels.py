from src.api.dependencies import PaginationDep
from fastapi import APIRouter, Query, Body, HTTPException, status

from src.schemas.hotels import Hotel, HotelPatch
from src.database import async_session_maker, engine

from repositories.hotels import HotelsRepository

router = APIRouter()


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название Отеля"),
        location: str | None = Query(None, description="Локация отеля")
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_by_id(id=hotel_id)
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

        return hotel


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 5 звезд у моря",
            "location": "Сочи, ул.Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель у фонтана",
            "location": "Дубай, ул.Шейха, 2"
        }
    },
    "3": {
        "summary": "Россия",
        "value": {
            "title": "Отель весенний",
            "location": "Краснодар, ул. Мира, 65"
        }
    },
    "4": {
        "summary": "Россия",
        "value": {
            "title": "Отель октябрьский",
            "location": "Москва, ул. Некрасова, 65"
        }
    },

})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)

        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel_all_values(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if len(hotel) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        if len(hotel) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="More than one")

        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "OK"}


@router.patch("{hotel_id}", summary="частичное обновление даных об отеле")
async def change_hotel_value(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        return {"message": "Successfully changed"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if len(hotel) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        if len(hotel) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="More than one")

        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "OK"}
