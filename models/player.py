# ID 	Int 	Первичный ключ, автоинкремент
# Name 	Varchar 	Имя игрока

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .database import BaseModel

class PlayerModel(BaseModel):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), index=True)
