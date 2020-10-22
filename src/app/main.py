from fastapi import FastAPI

from app.api import person


app = FastAPI()


app.include_router(person.router)
