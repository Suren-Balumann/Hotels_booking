from typing import Annotated
from src.api.dependencies import PaginationDep
from fastapi import APIRouter, Query, Body

from src.models.hotels import HotelOrm
from src.schemas.hotels import Hotel, HotelPatch
from src.database import async_session_maker, engine
from sqlalchemy import insert, select

router = APIRouter()


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название Отеля"),
        location: str | None = Query(None, description="Локация отеля")
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        query = select(HotelOrm)

        if title:
            query = query.filter(HotelOrm.title.ilike(f'%{title}%'))

        if location:
            query = query.filter(HotelOrm.location.ilike(f'%{location}%'))

        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


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
        add_hotel_stmt = insert(HotelOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def change_hotel_all_values(hotel_id: int, hotel_data: Hotel):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name

    return {"message": "successfully changed!", "data": hotel}


@router.patch("{hotel_id}", summary="частичное обновление даных об отеле")
def change_hotel_value(hotel_id: int, hotel_data: HotelPatch):
    data = None
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            data = hotel

    return {"message": "Successfully changed", "data": data}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
