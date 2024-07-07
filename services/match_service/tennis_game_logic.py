from enum import IntEnum

from utils.uuid import get_uuid

class GameScore(IntEnum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FOURTY = 3
    GAME_OR_AD = 4
    AD_WIN = 5


class Match:
    def __init__(self, p1_id: int, p2_id: int) -> None:
        self.match_uuid = get_uuid()
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.sets = [
            [0,0],
            [0,0],
            [0,0]
        ]
        self.cur_set = 0
        self.p1_game_score: GameScore|int = GameScore.LOVE
        self.p2_game_score: GameScore|int = GameScore.LOVE
        self.is_tiebreak = False
        self.is_match_end = False
        self.winner_id: int|None = None 

    def add_game_point(self, player_num: int) -> None:
        cur_score = getattr(self, f"p{player_num}_score")
        setattr(self, f"p{player_num}_score", cur_score + 1)
        if (
            self.p1_game_score == GameScore.GAME_OR_AD and
            self.p2_game_score == GameScore.GAME_OR_AD
        ):
            self.p1_game_score = GameScore.FOURTY
            self.p2_game_score = GameScore.FOURTY

        if self.is_game_end():
            self.sets[self.cur_set][player_num-1] += 1 # [2-1] = [1], [1-1] = [0]
            self.p1_game_score = GameScore.LOVE
            self.p2_game_score = GameScore.LOVE

        if self.is_set_end():
            self.cur_set += 1
            if self.cur_set == 3:
                self.is_match_end = True
                self.set_winner()
        
    def is_game_end(self) -> bool:
        scores = (self.p1_game_score, self.p2_game_score)

        if (
            not self.is_tiebreak and 
            any([score == GameScore.GAME_OR_AD for score in scores]) and
            abs(scores[0] - scores[1]) >= 2
        ):
            return True
        
        if (
            not self.is_tiebreak and
            any([score == GameScore.AD_WIN for score in scores])
        ):
            return True
        
        if (
            self.is_tiebreak and
            any([score >= 7 for score in scores]) and
            abs(scores[0] - scores[1]) >= 2
        ):
            return True
        
        return False

    def is_set_end(self) -> bool:
        p1_games_won = self.sets[self.cur_set][0]
        p2_games_won = self.sets[self.cur_set][1]

        if (
            any([p == 6 for p in (p1_games_won, p2_games_won)]) and
            abs(p1_games_won - p2_games_won) >= 2
        ):
            return True

        if (
            any([p == 7 for p in (p1_games_won, p2_games_won)])
        ):
            self.is_tiebreak = False
            return True
        
        if p1_games_won == 6 and p2_games_won == 6:
            self.is_tiebreak = True
        
        return False

    def set_winner(self) -> None:
        p1_sets_won = 0
        p2_sets_won = 0
        for set_result in self.sets:
            if set_result[0] > set_result[1]:
                p1_sets_won += 1
            else:
                p2_sets_won += 1
        
        if p1_sets_won > p2_sets_won:
            self.winner_id = self.p1_id
        else:
            self.winner_id = self.p2_id

