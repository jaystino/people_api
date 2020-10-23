from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.sql import and_

from app.api.models import PersonCreateIn
from app.db import database, persons


async def insert_person(
    person: PersonCreateIn, person_id: UUID, version: int, is_latest: bool
):
    query = persons.insert().values(
        person_id=person_id,
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        email=person.email,
        age=person.age,
        version=version,
        is_latest=is_latest,
    )
    return await database.execute(query=query)


async def select_person(person_id: UUID, version: Optional[int] = None):
    if not version:
        query = persons.select().where(person_id == persons.c.person_id)
    else:
        query = persons.select().where(
            and_(person_id == persons.c.person_id, version == persons.c.version)
        )
    if record := await database.fetch_one(query=query):
        return dict(record)
    return None


async def select_persons():
    query = persons.select()
    if records := await database.fetch_all(query=query):
        targets = [
            "record",
            "person_id",
            "first_name",
            "last_name",
            "version",
            "is_latest",
        ]
        recs = [
            {
                k: (lambda x: str(x) if isinstance(x, UUID) else x)(v)
                for k, v in rec.items()
                if k in targets
            }
            for rec in records
        ]
        return recs
