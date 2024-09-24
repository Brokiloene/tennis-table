# from typing import List
from sqlalchemy import select

from tennis_app.src.models import PlayerModel
from tennis_app.src.shared.exceptions import PlayerNotFoundError
from tennis_app.src.shared.dto import ReadPlayerDTO

from tennis_app.src.shared.core import BaseDAO

class PlayerDAO(BaseDAO):
    def insert_one(name: str) -> int:
        with BaseDAO.new_session() as session:
            stmt = select(PlayerModel).filter_by(name=name)
            player = session.execute(stmt).scalar_one_or_none()
            if player is None:
                player = PlayerModel(name=name)
                session.add(player)
                session.commit()

        return player.id

    def select_one_by_name(name: str) -> ReadPlayerDTO:
        """
        :raises: PlayerNotFoundError
        """
        with BaseDAO.new_session() as session:
            stmt = select(PlayerModel).filter_by(name=name)
            player = session.execute(stmt).scalar()
        if player is None:
            raise PlayerNotFoundError("error info here")
        else:
            return ReadPlayerDTO(p_id=player.id, name=player.name)
        