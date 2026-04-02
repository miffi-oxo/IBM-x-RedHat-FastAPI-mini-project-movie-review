from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class RatingBase(BaseModel):
    star:int | None=None

class ReatingCreate(RatingBase):
    pass

class RatingInDB(RatingBase):
    rat_id:int
    user_id:int
    mov_id:int
    
    class Config:
        from_attributes=True


class RatingRead(RatingInDB):
    pass