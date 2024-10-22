from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

from .database import BaseModel


class MatchModel(BaseModel):
    __tablename__ = "match"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36))
    player1_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"))
    winner_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"))
    score: Mapped[str] = mapped_column(String(11))  # example: '6 4 4 6 7 6'
