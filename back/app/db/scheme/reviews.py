from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class ReviewBase(BaseModel):
    content:str


class ReviewCreate(ReviewBase):
    pass

class ReviewInDB(ReviewBase):
    rev_id:int
    user_id:int
    mov_id:int
    rev_create:datetime

    class Config:
        from_attributes=True


class ReviewRead(ReviewInDB):
    pass