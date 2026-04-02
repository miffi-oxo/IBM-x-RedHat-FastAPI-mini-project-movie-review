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
    user_id:int
    