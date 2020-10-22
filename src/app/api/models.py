from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PersonReadIn(BaseModel):
    id_: UUID


class PersonOut(BaseModel):
    record: int
    id_: UUID
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
    id_: UUID
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


class PersonDeleteIn(BaseModel):
    id_: UUID


class PersonDeleteOut(BaseModel):
    success: bool


class PersonsOut(BaseModel):
    persons: List[PersonOut]
