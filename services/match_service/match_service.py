from utils import get_uuid
from .tennis_game_logic import Match

class MatchService:
    ongoing_matches = {}
    def create_match(p1_name: str, p2_name: str):
        match_uuid = get_uuid()
        MatchService.ongoing_matches[match_uuid] = Match(p1_name, p2_name)
        return match_uuid
