from src.api.dependencies import PaginationDep, DBDep, DatesDep
from fastapi import APIRouter, Query, Body

from src.api.examples.hotels import post_example
from src.exceptions import ObjectNotFoundException, HotelNotFoundHttpException
from src.schemas.hotels import HotelAdd, HotelPatch
from fastapi_cache.decorator import cache

from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        dates: DatesDep,
        title: str | None = Query(None, description="Название Отеля"),
        location: str | None = Query(None, description="Локация отеля"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        dates,
        title,
        location
    )


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHttpException

    return hotel


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples=post_example
        ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel_all_values(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHttpException

    await HotelService(db).edit_hotel(hotel.id, hotel_data)
    return {"status": "OK"}


@router.patch("{hotel_id}", summary="частичное обновление даных об отеле")
async def change_hotel_value(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_data, hotel_id)
    return {"message": "Successfully changed"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
