import itertools

from tennis_app.src.shared.tennis_game_logic import Match


class MatchToDictSerializer:
    @staticmethod
    def serialize(match_obj: Match) -> dict:
        p1_game_score: str = Match.game_score_to_str(match_obj.p1_game_score)
        p2_game_score: str = Match.game_score_to_str(match_obj.p2_game_score)
        if match_obj.match_ended:
            cur_set_score: list = match_obj.sets[2]
        else:
            cur_set_score: list = match_obj.sets[match_obj.cur_set]

        d = {
            "name_p1": match_obj.p1_name,
            "name_p2": match_obj.p2_name,
            "p1_digit_1": p1_game_score[0],
            "p1_digit_2": p1_game_score[1],
            "p2_digit_1": p2_game_score[0],
            "p2_digit_2": p2_game_score[1],
            "cur_set_p1": cur_set_score[0],
            "cur_set_p2": cur_set_score[1],
        }

        if match_obj.is_tiebreak:
            d["match_status"] = "tiebreak"
        elif match_obj.match_ended:
            d["match_status"] = "match is over"
        else:
            d["match_status"] = "match is ongoing"

        keys = ["set1_p1", "set1_p2", "set2_p1", "set2_p2", "set3_p1", "set3_p2"]
        vals = itertools.chain(*match_obj.sets)
        d |= {k: v for k, v in zip(keys, vals)}
        return d

    @staticmethod
    def get_only_result_data(match_obj: Match) -> str:
        sets_flatten = itertools.chain(*match_obj.sets)
        return " ".join(map(str, sets_flatten))
