from datetime import date
from src.api.dependencies import PaginationDep, DBDep
from fastapi import APIRouter, Query, Body, HTTPException, status
from src.schemas.hotels import HotelAdd, HotelPatch
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
# @cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название Отеля"),
        location: str | None = Query(None, description="Локация отеля"),
        date_from: date = Query(example="2025-05-01"),
        date_to: date = Query(example="2025-05-04"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        title=title,
        location=location,
        limit=per_page,
        offset=(pagination.page - 1) * per_page,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel_by_id(
        hotel_id: int,
        db: DBDep
):
    hotel = await db.hotels.get_by_id(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return hotel


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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

        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel_all_values(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if len(hotel) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if len(hotel) > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="More than one")

    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("{hotel_id}", summary="частичное обновление даных об отеле")
async def change_hotel_value(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep
):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"message": "Successfully changed"}


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
        db: DBDep
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if len(hotel) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if len(hotel) > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="More than one")

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
