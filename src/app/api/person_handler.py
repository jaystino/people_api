from asyncpg.exceptions import DataError
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from app.api.dal import insert_person, select_person
from app.api.models import Person, PersonCreateIn, PersonDeleteOut, PersonUpdateIn

router = APIRouter()


@router.get("/{person_id}", response_model=Person)
async def read_person(person_id: UUID, version: Optional[int] = None):
    """GET a single person record. By default returns the most current version, unless
    the version is specified.

    :param person_id: person uuid
    :param version: target person version
    :return: a person record
    """
    try:
        record = await select_person(person_id, version)
    except Exception as e:  # TODO: remove bare exception
        raise e
    if not record:
        if version:
            message = f"no version {version} record found for person_id {person_id}"
        else:
            message = f"no record found for person_id {person_id}"
        raise HTTPException(status_code=404, detail=message)
    return record


@router.post("/", response_model=Person, status_code=201)
async def create_person(person_in: PersonCreateIn):
    """POST a new person with a unique id.

    :param person_in: PersonCreateIn object
    :return: Person instance if success, else 400
    """
    person_id = uuid4()
    version = 1
    is_latest = True
    try:
        record_id = await insert_person(person_in, person_id, version, is_latest)
        return dict(
            record=record_id,
            person_id=person_id,
            first_name=person_in.first_name,
            middle_name=person_in.middle_name,
            last_name=person_in.last_name,
            email=person_in.email,
            age=person_in.age,
            version=version,
            is_latest=is_latest,
        )
    except (DataError, NameError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/", response_model=Person)
async def update_person(person: PersonUpdateIn):
    return Person


@router.delete("/{person_id}", response_model=PersonDeleteOut)
async def delete_person(person_id: UUID):
    return PersonDeleteOut
