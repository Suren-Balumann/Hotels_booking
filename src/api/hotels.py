from typing import Annotated
from src.api.dependencies import PaginationDep
from fastapi import APIRouter, Query
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Laguna"},
    {"id": 2, "title": "Дубай", "name": "Grand"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название Отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue

        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        start_index = (pagination.page - 1) * pagination.per_page
        end_index = start_index + pagination.per_page
        return hotels_[start_index:end_index]

    return hotels_


@router.post("")
def create_hotel(hotel_data: Hotel):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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
