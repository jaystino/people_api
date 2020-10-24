from asyncpg.exceptions import DataError
from typing import Dict, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from app.api.dal import (
    drop_person,
    insert_person,
    select_latest_version,
    select_person,
    update_is_latest,
)
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
        record = await insert_person(person_in, person_id, version, is_latest)
        return _format_person_response(person_in, record, person_id, version, is_latest)
    except (DataError, NameError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/", response_model=Person)
async def update_person(person: PersonUpdateIn):
    # fetch latest record
    current_person = await select_person(person.person_id)
    if not current_person:
        message = (
            "cannot update person, no records with person_id "
            f"{person.person_id} found"
        )
        raise HTTPException(status_code=404, detail=message)
    # ensure request contains updates compared to current_person
    updates = {k: v for k, v in dict(person).items() if v and v != current_person[k]}
    if not updates:
        raise HTTPException(status_code=400, detail="no new attributes to update")

    # set current version is_latest to False
    # if not await update_latest(False, record=current_person.get("record")):
    #     raise HTTPException(
    #         status_code=500, detail="failed to deactivate previous version"
    #     )
    if not await update_latest(person_id=person.person_id):
        raise HTTPException(
            status_code=500, detail="failed to deactivate previous version"
        )

    # "update" new version
    new_version = current_person.get("version") + 1
    updated_person = PersonCreateIn(
        first_name=updates.get("first_name", current_person.get("first_name")),
        middle_name=updates.get("middle_name", current_person.get("middle_name")),
        last_name=updates.get("last_name", current_person.get("last_name")),
        email=updates.get("email", current_person.get("email")),
        age=updates.get("age", current_person.get("age")),
    )
    record = await insert_person(
        updated_person, person.person_id, new_version, is_latest=True
    )

    return _format_person_response(
        updated_person, record, person.person_id, new_version, True
    )


@router.delete("/{person_id}", response_model=PersonDeleteOut)
async def delete_person(person_id: UUID):
    """DELETE the latest version corresponding to the given person_id.

    :param person_id: person UUID
    :return: dict stating success, else HTTPException
    """
    # fetch and delete latest record
    if latest_version := await select_latest_version(person_id):
        await drop_person(person_id, latest_version)
        if latest_version == 1:
            return {"success": True}  # 1 is the lowest possible version
    else:
        message = f"cannot delete record, no records with person_id {person_id} found"
        raise HTTPException(status_code=404, detail=message)

    # set previous version is_latest to True
    if not await update_is_latest(
        person_id=person_id, version=(latest_version - 1), set_latest=True
    ):
        # TODO: make this transactional. Will corrupt data if failure at this point.
        raise HTTPException(status_code=500, detail="versioning error")

    return {"success": True}


def _format_person_response(
    person_in: PersonCreateIn,
    record: int,
    person_id: UUID,
    version: int,
    is_latest: bool,
) -> Dict:
    """Format the person response object.

    :param person_in: PersonCreateIn object
    :param record: record number
    :param person_id: person UUID
    :param version: version for associated person_id
    :param is_latest: bool indicating if specified version is the most current
    :return:
    """
    return dict(
        record=record,
        person_id=person_id,
        first_name=person_in.first_name,
        middle_name=person_in.middle_name,
        last_name=person_in.last_name,
        email=person_in.email,
        age=person_in.age,
        version=version,
        is_latest=is_latest,
    )
