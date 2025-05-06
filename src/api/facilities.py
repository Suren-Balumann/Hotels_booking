from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix='/facilities', tags=["Удобства"])


@router.post("")
async def add_facility(
        db: DBDep,
        data: FacilitiesAdd = Body(openapi_examples={
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
