from typing import Dict, List, Optional, Union
from uuid import UUID

from sqlalchemy.sql import and_, func, select as gen_select

from app.api.models import Person, PersonCreateIn
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
            and_(persons.c.person_id == person_id, persons.c.version == version)
        )
    if record := await database.fetch_one(query=query):
        return dict(record)


async def update_is_latest(person_id: UUID, version: int, set_latest: bool) -> Person:
    """Update the is_latest bool column for a single person record.

    :param person_id: person UUID
    :param version: target version
    :param set_latest: target is_latest status
    :return: Person object
    """
    query = (
        persons.update()
        .where(and_(persons.c.person_id == person_id, persons.c.version == version))
        .values(is_latest=set_latest)
        .returning(
            persons.c.record,
            persons.c.person_id,
            persons.c.first_name,
            persons.c.middle_name,
            persons.c.last_name,
            persons.c.email,
            persons.c.age,
            persons.c.version,
            persons.c.is_latest,
        )
    )
    return await database.execute(query=query)


async def drop_person(person_id: UUID, version: int):
    """Delete a single person record from the persons table.

    :param person_id: person UUID
    :param version: record version
    :return:
    """
    query = persons.delete().where(
        and_(persons.c.person_id == person_id, persons.c.version == version)
    )
    await database.execute(query=query)


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


async def select_latest_version(person_id: UUID) -> int:
    """Selects the latest version for the given person_id.

    :param person_id: person UUID
    :return: version for given person_id
    """
    query = gen_select([func.max(persons.c.version)]).where(
        persons.c.person_id == person_id
    )
    record = await database.fetch_one(query=query)
    return record.get("max_1")
