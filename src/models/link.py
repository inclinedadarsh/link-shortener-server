from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import AnyHttpUrl, field_validator


class LinkBase(SQLModel):
    link: str = Field(unique=True, index=True)

    @field_validator("link")
    def validate_url(cls, v):
        AnyHttpUrl(v)
        return v


class Link(LinkBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    short: str = Field(unique=True, index=True)


class LinkCreate(LinkBase):
    pass
