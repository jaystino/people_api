from fastapi import APIRouter

router = APIRouter()


@router.get("/person")
async def read_person():
    return {"first_name": "guido"}
