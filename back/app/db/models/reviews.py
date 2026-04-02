from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional , List , TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
    from .movies import Movie
    from .comments import Comment


class Review(Base):
    __tablename__="reviews"

    rev_id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.user_id"), nullable=False)
    mov_id:Mapped[int]=mapped_column(ForeignKey("movies.mov_id"),nullable=False)
    content:Mapped[str]=mapped_column(String(255), nullable=False)
    rev_create:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="reviews")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="reviews")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="review")