from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.api.examples.facilities import post_example
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService
# from src.utils.cache_decorator import my_own_cache
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("")
async def add_facility(
    db: DBDep,
    data: FacilityAdd = Body(
        openapi_examples=post_example
    ),
):
    facility = await FacilityService(db).add_facility(data)
    return {"status": "OK", "data": facility}


@router.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()
