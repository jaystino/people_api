from uuid import UUID

from app.api import models

person_record = models.Person(
    record=1,
    person_id=UUID("5f2f95ab-8683-49ea-a755-50273c956e66"),
    first_name="a",
    last_name="b",
    email="a@b.com",
    age=20,
    version=2,
    is_latest=True,
)

valid_person_response = {
    "record": 1,
    "person_id": UUID("5f2f95ab-8683-49ea-a755-50273c956e66"),
    "first_name": "a",
    "last_name": "b",
    "middle_name": None,
    "email": "a@b.com",
    "age": 20,
    "is_latest": True,
    "version": 2,
}

persons_record = [
    dict(
        record=1,
        person_id=UUID("5f2f95ab-8683-49ea-a755-50273c956e66"),
        first_name="a",
        last_name="b",
        version=2,
        is_latest=True,
    )
]

valid_persons_response = {
    "persons": [
        {
            "first_name": "a",
            "is_latest": True,
            "last_name": "b",
            "person_id": "5f2f95ab-8683-49ea-a755-50273c956e66",
            "record": 1,
            "version": 2,
        }
    ]
}
