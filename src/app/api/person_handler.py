from typing import Optional
from uuid import UUID

from fastapi import APIRouter

from app.api.dal import insert_person
from app.api.models import (
    Person,
    PersonCreateIn,
    PersonDeleteOut,
    PersonsOut,
    PersonUpdateIn,
)

router = APIRouter()


@router.get("/{person_id}", response_model=Person)
async def read_person(person_id: UUID, version: Optional[int] = None):
    return Person


@router.post("/", response_model=Person, status_code=201)
async def create_person(person: PersonCreateIn):
    await insert_person(person)


@router.put("/", response_model=Person)
async def update_person(person: PersonUpdateIn):
    return Person


@router.delete("/{person_id}", response_model=PersonDeleteOut)
async def delete_person(person_id: UUID):
    return PersonDeleteOut


@router.get("/persons/", response_model=PersonsOut)
async def read_person():
    return PersonsOut
