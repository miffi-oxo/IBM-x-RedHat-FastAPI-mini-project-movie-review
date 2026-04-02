from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .reviews import Review
    from .ratings import Rating
    from .comments import Comment

class User(Base):
    __tablename__="users"

    user_id:Mapped[int]=mapped_column(primary_key=True)
    user_name:Mapped[str]=mapped_column(String(50))
    email:Mapped[str]=mapped_column(String(100), unique=True, nullable=False)
    password:Mapped[str]=mapped_column(String(50), nullable=False)
    ref_token:Mapped[str]=mapped_column(String(255), nullable=True)
    user_create:Mapped[datetime]=mapped_column(TIMESTAMP,server_default=func.now(), nullable=False)


    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")