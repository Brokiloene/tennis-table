import threading
from typing import Dict, List

from utils import get_uuid, UUID
from exceptions import MatchNotFoundError
from .tennis_game_logic import Match

class MatchService:
    ongoing_matches: Dict[UUID, Match] = {}
    ended_matches_uuid: List[UUID] = []
    lock = threading.Lock()

    def create_match(p1_name: str, p2_name: str):
        match_uuid = get_uuid()
        with MatchService.lock:
            MatchService.ongoing_matches[match_uuid] = Match(p1_name, p2_name)
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
        # здесь взаимодействия с DAO и сохранение матча


        need_to_clear_cache = False
        with MatchService.lock:
            MatchService.ended_matches_uuid.append(match_uuid)
            if len(MatchService.ended_matches_uuid) >= 10:
                need_to_clear_cache = True
        
        if need_to_clear_cache:
            MatchService._clear_ended_matches_from_cache() # untested


    def _clear_ended_matches_from_cache(self):
        with MatchService.lock:
            for uuid in MatchService.ended_matches_uuid:
                del MatchService.ongoing_matches[uuid]
