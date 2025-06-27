from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task

class FacilityService(BaseService):

    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data=data)
        await self.db.commit()

        # test_task.apply_async(args=["Hello my pretty baby"], countdown=20)
        test_task.delay("Hello my pretty baby")
        return facility
