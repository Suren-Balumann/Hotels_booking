from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix='/facilities', tags=["Удобства"])


@router.post("")
async def add_facility(
        db: DBDep,
        data: FacilityAdd = Body(openapi_examples={
            "1": {
                "summary": "Кондиционер",
                "value": {
                    "title": "Кондиционер"
                }
            },
            "2": {
                "summary": "WiFi",
                "value": {
                    "title": "WiFi"
                }
            },
            "3": {
                "summary": "Бассейн",
                "value": {
                    "title": "Бассейн"
                }
            },
        })
):
    facility = await db.facilities.add(data=data)
    await db.commit()
    return {"status": "OK", "data": facility}


@router.get("")
async def get_all_facilities(
        db: DBDep
):
    return await db.facilities.get_all()


# @router.get("/{room_id}")
# async def get_rooms_facilities(
#         room_id: int,
#         db: DBDep
# ):
#     room_data = [3, 4]
#     exists_facilities_ids = await db.rooms_facilities.get_ficilities_ids(room_id=room_id)
#     data_facilities_ids = list(set(room_data + exists_facilities_ids))
#     print(data_facilities_ids)
