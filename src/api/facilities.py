from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.utils.cache_decorator import my_own_cache
from src.tasks.tasks import test_task

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

    # test_task.apply_async(args=["Hello my pretty baby"], countdown=20)
    # test_task.delay("Hello my pretty baby")
    return {"status": "OK", "data": facility}


@router.get("")
# @my_own_cache(expire=10)
async def get_all_facilities(
        db: DBDep
):
    return await db.facilities.get_all()
