from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from typing import Optional , List , TYPE_CHECKING
if TYPE_CHECKING:
    from .reviews import Review
    from .ratings import Rating

class Movie(Base):
    __tablename__="moives"

    mov_id:Mapped[int]=mapped_column(primary_key=True)
    mov_name:Mapped[str]=mapped_column(String(50),nullable=False)
    mov_descript:Mapped[str]=mapped_column(String(255),nullable=False)
    mov_release:Mapped[datetime]=mapped_column(TIMESTAMP, nullable=False)
    genre:Mapped[str]=mapped_column(String(50),nullable=False)

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="movie")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="movie")
