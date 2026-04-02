from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated

class UserBase(BaseModel):
    user_name:str
    email:str
    password:str
    
class UserCreate(BaseModel):
    user_name:str
    email:str
    password:  Annotated[str, Field(max_length=72)]

class UserLogin(BaseModel):
    email:str
    password: Annotated[str, Field(max_length=72)]


class UserUpdate(BaseModel):
    user_id:int | None=None
    user_name:str | None=None
    password: str | None=None

class UserInDB(UserBase):
    user_id: int
    user_create: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    #sqlalchemy객체를 pydantic모델로 변환할때 사용
    class Config:
        from_attributes = True

class UserRead(UserInDB):
    pass

    