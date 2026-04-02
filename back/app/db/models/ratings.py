from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey, Integer
from typing import Optional , List , TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
    from .movies import Movie


class Rating(Base):
    __tablename__="ratings"

    rat_id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.user_id"), nullable=False)
    mov_id:Mapped[int]=mapped_column(("movies.mov_id"),nullable=False)
    star: Mapped[Optional[int]]=mapped_column(Integer(5),nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="ratings")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="ratings")