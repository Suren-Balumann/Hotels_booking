import logging
from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import NoResultFound, IntegrityError

from asyncpg.exceptions import UniqueViolationError
from src.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
)
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filter_by(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        result = [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]
        return result

    async def get_all(self, *args, **kwargs):
        return await self.get_filter_by(**kwargs)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None

        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        # sqlalchemy.exc.NoResultFound
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        try:
            query = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(query)
            model = result.scalars().one()
        except IntegrityError as ex:
            logging.error(
                f"Не удалось добавить данные в БД, входные данные {data},тип ошибки: {type(ex.orig.__cause__)}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.error(
                    f"Незнакомая ошибка: Не удалось добавить данные в БД, входные данные {data},тип ошибки: {type(ex.orig.__cause__)}"
                )
                raise ex

        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        query = insert(self.model).values([item.model_dump() for item in data])
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        await self.session.execute(query)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
