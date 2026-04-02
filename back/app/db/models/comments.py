from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func , ForeignKey
from typing import Optional , List , TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
    from .reviews import Review

class Comment(Base):
    __tablename__="comments"

    com_id:Mapped[int]
    user_id:Mapped[int]=mapped_column(ForeignKey("users.user_id"), nullable=False)
    rev_id:Mapped[int]=mapped_column(ForeignKey("ratings.rav_id"), nullable=False)
    com_content:Mapped[str]=mapped_column(String(255), nullable=False)
    com_create: Mapped[Optional[datetime]]= mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    review: Mapped["Review"] = relationship("Review", back_populates="comments")