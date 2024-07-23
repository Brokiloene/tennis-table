from typing import List

from sqlalchemy import select

from dto import CreateMatchDTO, ReadMatchDTO
from models import MatchModel, PlayerModel
from .base import BaseDAO


class MatchDAO(BaseDAO):
    def insert_one(dto: CreateMatchDTO) -> None:
        with BaseDAO.new_session() as session:
            match_to_add = MatchModel(**dto.asdict())
            session.add(match_to_add)
            session.commit()

    def fetch_all() -> List[ReadMatchDTO]:
        matches_dtos = []
        with BaseDAO.new_session() as session:
            stmt = select(MatchModel)
            all_matches = session.execute(stmt).scalars().all()
            for match in all_matches:
                p1_name = session.get(PlayerModel, match.player1_id).name
                p2_name = session.get(PlayerModel, match.player2_id).name
                matches_dtos.append(ReadMatchDTO(
                    player1_name=p1_name,
                    player2_name=p2_name,
                    score=match.score
                ))
        print(matches_dtos)
        return matches_dtos
    
    def test_fill():
        players = [
            "Bjorn Borg", #1
            "John McEnroe", #2
            "Ivan Lendl", #3
            "Roger Federer", #4
            "Pete Sampras", #5
            "Rafael Nadal", #6
            "John Isner", #7
            "Nicolas Mahut", #8
            "Andre Agassi", #9
            "Fernando Verdasco", #10
            "Andy Roddick", #11
            "Novac Djokovic" #12
        ]
        matches = [
            CreateMatchDTO(
                uuid='',
                player1_id=1,
                player2_id=2,
                winner_id=1,
                score="1 6 7 5 6 3"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=2,
                player2_id=1,
                winner_id=2,
                score="4 6 7 6 7 6"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=3,
                player2_id=2,
                winner_id=3,
                score="3 6 7 5 7 5"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=4,
                player2_id=5,
                winner_id=5,
                score="5 7 6 4 6 7"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=6,
                player2_id=4,
                winner_id=6,
                score="6 4 6 7 6 4"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=7,
                player2_id=8,
                winner_id=7,
                score="6 4 3 6 7 6"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=5,
                player2_id=9,
                winner_id=5,
                score="6 7 7 6 7 6"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=6,
                player2_id=10,
                winner_id=6,
                score="6 7 6 4 7 6"
            ),
            CreateMatchDTO(
                uuid='',
                player1_id=4,
                player2_id=11,
                winner_id=4,
                score="5 7 7 6 7 6"
            ),
            # CreateMatchDTO(
            #     uuid='',
            #     player1_id=12,
            #     player2_id=6,
            #     winner_id=12,
            #     score="5 7 6 4 6 2"
            # )
        ]

        with BaseDAO.new_session() as session:
            for player_name in players:
                session.add(PlayerModel(name=player_name))
            session.commit()
            for match_data in matches:
                match_to_add = MatchModel(**match_data.asdict())
                session.add(match_to_add)
            session.commit()
                
