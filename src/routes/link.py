from src.models.link import Link, LinkCreate
from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from src.db import engine
import random
import string

router = APIRouter()


@router.get("/", response_model=List[Link], status_code=status.HTTP_200_OK)
def get_links():
    with Session(engine) as session:
        links = session.exec(select(Link)).all()
        return links


def generate_short_url(length: int = 5) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


@router.post("/", response_model=Link, status_code=status.HTTP_201_CREATED)
def post_link(link: LinkCreate):
    with Session(engine) as session:
        # Check if link already exists, if yes then retrun that
        existing_link = session.exec(select(Link).where(Link.link == link.link)).first()

        if existing_link:
            return existing_link
        # Generate a unique short URL
        while True:
            short_url = generate_short_url()
            # Check if the short URL already exists
            existing_link = session.exec(
                select(Link).where(Link.short == short_url)
            ).first()
            if not existing_link:
                break

        # Create the Link object with both the original URL and short URL
        db_link = Link(short=short_url, link=link.link)
        session.add(db_link)
        session.commit()
        session.refresh(db_link)
        return db_link


@router.get("/{link_short}", response_model=Link, status_code=status.HTTP_200_OK)
def get_link(link_short: str):
    with Session(engine) as session:
        existing_link = session.exec(
            select(Link).where(Link.short == link_short)
        ).first()

        if existing_link:
            return existing_link
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Link doesn't exist for this short!"
            )
