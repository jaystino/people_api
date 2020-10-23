from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PersonCreateIn(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    age: int


class Person(PersonCreateIn):
    record: int
    person_id: UUID
    version: int
    is_latest: bool


class PersonUpdateIn(BaseModel):
    person_id: UUID
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


class PersonDeleteOut(BaseModel):
    success: bool


class Persons(BaseModel):
    record: int
    person_id: str
    first_name: str
    last_name: str
    version: int
    is_latest: bool


class PersonsOut(BaseModel):
    persons: List[Persons]
