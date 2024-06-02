from pydantic import BaseModel, HttpUrl
from typing import Optional


class Query(BaseModel):
    query: Optional[str] = None


class Answer(BaseModel):
    answer: Optional[str] = None
    url: Optional[str] = None
