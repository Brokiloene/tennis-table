from enum import IntEnum


class GameScore(IntEnum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FOURTY = 3
    GAME_OR_AD = 4
    AD_WIN = 5


class Match:
    def __init__(self, p1_name: str, p2_name: str) -> None:
        self.p1_name: str = p1_name
        self.p2_name: str = p2_name
        self.sets: list[list[int]] = [[0, 0], [0, 0], [0, 0]]
        self.cur_set: int = 0
        self.p1_game_score: GameScore | int = GameScore.LOVE
        self.p2_game_score: GameScore | int = GameScore.LOVE
        self.p1_sets_won: int = 0
        self.p2_sets_won: int = 0
        self.points_added = 0

        self.is_tiebreak: bool = False
        self.match_ended: bool = False
        self.winner: str | None = None

    def get_player_idx(self, player_name: str):
        """
        :raises: ValueError
        """
        if player_name == self.p1_name:
            return 1
        elif player_name == self.p2_name:
            return 2
        else:
            raise ValueError(f"Player with name {player_name} not found")

    def add_game_point(self, player_num: int) -> None:
        self.points_added += 1
        
        # there are player 1 and player 2
        if self.match_ended:
            return
        cur_score: int = getattr(self, f"p{player_num}_game_score")
        if self.is_tiebreak:
            new_score: int = cur_score + 1
        else:
            new_score = GameScore(cur_score + 1)
        setattr(self, f"p{player_num}_game_score", new_score)
        if (
            isinstance(self.p1_game_score, GameScore)
            and isinstance(self.p2_game_score, GameScore)
            and self.p1_game_score == GameScore.GAME_OR_AD
            and self.p2_game_score == GameScore.GAME_OR_AD
        ):
            self.p1_game_score = GameScore.FOURTY
            self.p2_game_score = GameScore.FOURTY

        if self.is_game_end():
            self.sets[self.cur_set][player_num - 1] += 1  # [2-1] = [1], [1-1] = [0]
            self.p1_game_score = GameScore.LOVE
            self.p2_game_score = GameScore.LOVE

        if self.is_set_end():
            if self.is_tiebreak:
                self.is_tiebreak = False

            self.cur_set += 1
            cur_sets_won = getattr(self, f"p{player_num}_sets_won")
            setattr(self, f"p{player_num}_sets_won", cur_sets_won + 1)
            if self.is_match_end():
                self.match_ended = True
                self.set_winner()


    def is_game_end(self) -> bool:
        scores = (self.p1_game_score, self.p2_game_score)

        if (
            not self.is_tiebreak
            and any([score == GameScore.GAME_OR_AD for score in scores])
            and abs(scores[0] - scores[1]) >= 2
        ):
            return True

        if not self.is_tiebreak and any(
            [score == GameScore.AD_WIN for score in scores]
        ):
            return True

        if (
            self.is_tiebreak
            and any([score >= 7 for score in scores])
            and abs(scores[0] - scores[1]) >= 2
        ):
            return True

        return False

    def is_set_end(self) -> bool:
        p1_games_won = self.sets[self.cur_set][0]
        p2_games_won = self.sets[self.cur_set][1]

        if (
            any([p >= 6 for p in (p1_games_won, p2_games_won)])
            and abs(p1_games_won - p2_games_won) >= 2
        ):
            return True
        
        if (
            self.is_tiebreak and 
            any([p == 7 for p in (p1_games_won, p2_games_won)])
        ):
            return True

        if p1_games_won == 6 and p2_games_won == 6:
            self.is_tiebreak = True

        return False

    def is_match_end(self) -> bool:
        if self.p1_sets_won >= 2 or self.p2_sets_won >= 2:
            self.match_ended = True
            return True
        else:
            return False

    def set_winner(self) -> None:
        if self.p1_sets_won > self.p2_sets_won:
            self.winner = self.p1_name
        else:
            self.winner = self.p2_name

    @staticmethod
    def game_score_to_str(game_score: GameScore | int):
        if not isinstance(game_score, GameScore):
            res = str(game_score)
            if len(res) < 2:
                res = "0" + res
            return res
        else:
            match game_score:
                case GameScore.LOVE:
                    return "00"
                case GameScore.FIFTEEN:
                    return "15"
                case GameScore.THIRTY:
                    return "30"
                case GameScore.FOURTY:
                    return "40"
                case GameScore.GAME_OR_AD:
                    return "AD"
                case _:  # error
                    return "ER"
