# ID 	Int 	Первичный ключ, автоинкремент
# UUID 	String 	Уникальный айди матча
# Player1 	Int 	Айди первого игрока, внешний ключ на Players.ID
# Player2 	Int 	Айди второго игрока, внешний ключ на Players.ID
# Winner 	Int 	Айди победителя, внешний ключ на Players.ID
# Score 	String 	JSON представление объекта с текущим счётом в матче
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, func

from .database import BaseModel

class MatchModel(BaseModel):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36), index=True) 
    player1_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"))
    winner_id: Mapped[int] = mapped_column(ForeignKey("player.id", ondelete="CASCADE"))
    score: Mapped[str] = mapped_column(String(11)) # '6 4 4 6 7 6'
