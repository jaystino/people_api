from typing import Optional
from uuid import UUID

from fastapi import APIRouter

from app.api.models import (
    PersonCreateIn,
    PersonDeleteOut,
    PersonOut,
    PersonsOut,
    PersonUpdateIn,
)

router = APIRouter()


@router.get("/person/{person_id}", response_model=PersonOut)
async def read_person(person_id: UUID, version: Optional[int] = None):
    return PersonOut


@router.post("/person/", response_model=PersonOut)
async def create_person(person: PersonCreateIn):
    return PersonOut


@router.put("/person/", response_model=PersonOut)
async def update_person(person: PersonUpdateIn):
    return PersonOut


@router.delete("/person/{person_id}", response_model=PersonDeleteOut)
async def delete_person(person_id: UUID):
    return PersonDeleteOut


@router.get("/persons/", response_model=PersonsOut)
async def read_person():
    return PersonsOut
