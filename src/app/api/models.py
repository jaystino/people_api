from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# class PersonIn(BaseModel):
#     person_id: UUID


class PersonOut(BaseModel):
    record: int
    person_id: UUID
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    age: int
    version: int
    is_latest: bool


class PersonCreateIn(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    age: int


class PersonUpdateIn(BaseModel):
    person_id: UUID
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


class PersonDeleteOut(BaseModel):
    success: bool


class PersonsOut(BaseModel):
    persons: List[PersonOut]
