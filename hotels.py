from fastapi import APIRouter, Path, Body, Query
from schemas.hotels import Hotel, HotelPatch

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
def get_hotels(id: int | None = Query(None, description="Айдишник"),
               title: str | None = Query(None, description="Название Отеля"),
               page: int | None = Query(default=1),
               per_page: int | None = Query(default=3)):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue

        hotels_.append(hotel)
    if id is None and title is None:
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        hotels_ = hotels[start_index:end_index]

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
