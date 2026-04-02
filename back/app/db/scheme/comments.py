from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated

class CommentBase(BaseModel):
    com_content:str
    
class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    com_id: int
    user_id: int
    rev_id:int
    com_create:datetime

    class Config:
        from_attributes=True

class CommentRead(CommentInDB):
    pass