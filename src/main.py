from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(link_router, prefix="/links", tags=["links"])


@app.get("/")
def read_root():
    return {"hello": "world"}
