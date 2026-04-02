from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class MovieBase(BaseModel):
    mov_name:str
    mov_discript:str
    mov_release:datetime
    genre:str

class MovieCreate(MovieBase):
    pass

class MovieInDB(MovieBase):
    mov_id:int

    class Config:
        from_attributes=True

class MovieRead(MovieInDB):
    pass
