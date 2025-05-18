from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up...")
    create_db_and_tables()

    yield
    print("Application is closing...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"hello": "world"}
