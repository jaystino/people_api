from fastapi import APIRouter, HTTPException

from app.api.dal import select_persons
from app.api.models import PersonsOut

router = APIRouter()


@router.get("/", response_model=PersonsOut)
async def read_persons():
    try:
        record = await select_persons()
    except Exception as e:  # TODO: remove bare exception
        raise e
    if not record:
        raise HTTPException(status_code=404, detail="no records found")
    return {"persons": record}
