from datetime import datetime
from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=200)
    role: str = Field(..., min_length=1, max_length=200)
    status: str = Field(default="applied", max_length=50)
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, min_length=1, max_length=200)
    status: str | None = Field(default=None, max_length=50)
    notes: str | None = None


class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
