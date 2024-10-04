from typing import List

from sqlalchemy import select, text

from tennis_app.src.shared.dto import CreateMatchDTO, ReadMatchDTO
from tennis_app.src.shared.core import BaseDAO
from tennis_app.src.models import MatchModel, PlayerModel


class MatchDAO(BaseDAO):
    def insert_one(dto: CreateMatchDTO) -> None:
        with BaseDAO.new_session() as session:
            match_uuid = dto.uuid
            stmt = select(MatchModel.id).filter_by(uuid=match_uuid)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                match_to_add = MatchModel(**dto.asdict())   
                session.add(match_to_add)
                session.commit()

    def fetch_all() -> List[ReadMatchDTO]:
        matches_data = []
        with BaseDAO.new_session() as session:
            stmt = text(
                """
                select m.score, p1.name, p2.name 
                from `match` m, player p1, player p2
                where m.player1_id = p1.id and m.player2_id = p2.id
                order by m.id
                """
            )
            matches_data = session.execute(stmt)
        matches_dtos = []
        for score, name1, name2 in matches_data:
            matches_dtos.append(ReadMatchDTO(
                player1_name=name1,
                player2_name=name2,
                score=score
            ))
        return matches_dtos
    
    def fetch_filtered(search_query: str):
        matches_data = []
        with BaseDAO.new_session() as session:
            stmt = text(
                """
                select m.score, p1.name, p2.name 
                from `match` m, player p1, player p2
                where m.player1_id = p1.id and m.player2_id = p2.id and
                (p1.name LIKE :search_query or p2.name LIKE :search_query) 
                order by m.id
                """
            )
            print("--------------------__> ", search_query)
            matches_data = session.execute(stmt, {"search_query": f"%{search_query}%"})
        matches_dtos = []
        for score, name1, name2 in matches_data:
            matches_dtos.append(ReadMatchDTO(
                player1_name=name1,
                player2_name=name2,
                score=score
            ))

        return matches_dtos
