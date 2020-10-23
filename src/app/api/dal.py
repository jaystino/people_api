from typing import Dict, List, Optional, Union
from uuid import UUID

from sqlalchemy.sql import and_

from app.api.models import PersonCreateIn
from app.db import database, persons


async def insert_person(
    person: PersonCreateIn, person_id: UUID, version: int, is_latest: bool
) -> int:
    """Insert a new person record with a unique person_id into the persons table.

    :param person: PersonCreateIn object
    :param person_id: uuid of person
    :param version: version of record for given person_id
    :param is_latest: bool indicating this the latest version the given person_id
    :return: record id
    """
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


async def select_person(
    person_id: UUID, version: Optional[int] = None
) -> Union[Dict, None]:
    """Fetch a single person record for the given person_id. Defaults to the latest
    version unless provided.

    :param person_id: uuid of person
    :param version: target record version
    :return: a single person record
    """
    if not version:
        query = persons.select().where(
            and_(persons.c.person_id == person_id, persons.c.is_latest == True)
        )
    else:
        query = persons.select().where(
            and_(person_id == persons.c.person_id, version == persons.c.version)
        )
    if record := await database.fetch_one(query=query):
        return dict(record)


async def select_persons() -> Union[List[Dict], None]:
    """Fetch the latest versions of all person records.

    :return: list of person records
    """
    query = persons.select()
    if records := await database.fetch_all(query=query):
        recs = [
            {
                k: (lambda x: str(x) if isinstance(x, UUID) else x)(v)
                for k, v in rec.items()
            }
            for rec in records
        ]
        return recs
