# from typing import List
from sqlalchemy import select

from models import PlayerModel
from exceptions import PlayerNotFoundError
from dto import ReadPlayerDTO

from .base import BaseDAO

class PlayerDAO(BaseDAO):
    def insert_one(name: str) -> int:
        with BaseDAO.new_session() as session:
            stmt = select(PlayerModel).filter_by(name=name)
            player = session.execute(stmt).scalar()
            session.flush()
            if player is None:
                player = PlayerModel(name=name)
                session.add(player)
                session.flush()
                session.commit()
                # print("===>", player.name, player.id)
            # else:
                # print("==->", player.name, player.id)

        print("===>", player.name, player.id)
        return player.id

    def select_one_by_name(name: str) -> ReadPlayerDTO:
        with BaseDAO.new_session() as session:
            stmt = select(PlayerModel).filter_by(name=name)
            player = session.execute(stmt).scalar()
        if player is None:
            raise PlayerNotFoundError("error info here")
        else:
            return ReadPlayerDTO(p_id=player.id, name=player.name)
        