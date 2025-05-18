from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import create_db_and_tables
from src.routes.link import router as link_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up...")
    create_db_and_tables()

    yield
    print("Application is closing...")


app = FastAPI(lifespan=lifespan)


app.include_router(link_router, prefix="/links", tags=["links"])


@app.get("/")
def read_root():
    return {"hello": "world"}
