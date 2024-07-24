import threading
from typing import Dict, List

from tennis_app.utils import get_uuid, UUID
from tennis_app.exceptions import MatchNotFoundError, PlayerNamesAreTheSameError
from tennis_app.dao import PlayerDAO, MatchDAO
from tennis_app.dto import CreateMatchDTO
from .tennis_game_logic import Match

class MatchService:
    ongoing_matches: Dict[UUID, Match] = {}
    ended_matches_uuid: List[UUID] = []
    lock = threading.Lock()

    def create_match(p1_name: str, p2_name: str):
        if p1_name == p2_name:
            raise PlayerNamesAreTheSameError()

        match_uuid = get_uuid()
        with MatchService.lock:
            PlayerDAO.insert_one(p1_name)
            PlayerDAO.insert_one(p2_name)
            MatchService.ongoing_matches[match_uuid] = Match(p1_name, p2_name)
        print(MatchService.ongoing_matches)
        return match_uuid
    
    def match_add_point(match_uuid: UUID, player_num: int) -> None:
        with MatchService.lock:
            try:
                MatchService.ongoing_matches[match_uuid].add_game_point(player_num)
            except KeyError:
                raise MatchNotFoundError
            
    def get_match_data(match_uuid: UUID) -> Dict[str, str]:
        with MatchService.lock:
            return MatchService.ongoing_matches[match_uuid].serialize()

    def save_finished_match(match_uuid: UUID):
        with MatchService.lock:
            match_obj = MatchService.ongoing_matches[match_uuid]
            match_result = match_obj.get_result_data()
            p1_name = match_obj.p1_name
            p2_name = match_obj.p2_name
            p1_id = PlayerDAO.select_one_by_name(p1_name).p_id
            p2_id = PlayerDAO.select_one_by_name(p2_name).p_id
            if p1_name == match_obj.winner:
                winner_id = p1_id
            else:
                winner_id = p2_id
            
            dto = CreateMatchDTO(
                uuid=str(match_uuid), 
                player1_id=p1_id, 
                player2_id=p2_id, 
                winner_id=winner_id, 
                score=match_result
                )

            MatchDAO.insert_one(dto)

        need_to_clear_cache = False
        with MatchService.lock:
            if match_uuid not in MatchService.ended_matches_uuid:
                MatchService.ended_matches_uuid.append(match_uuid)
            if len(MatchService.ended_matches_uuid) >= 10:
                need_to_clear_cache = True
        
        if need_to_clear_cache:
            MatchService._clear_ended_matches_from_cache() # untested


    def _clear_ended_matches_from_cache():
        with MatchService.lock:
            for uuid in MatchService.ended_matches_uuid:
                del MatchService.ongoing_matches[uuid]
