import pytest

from tennis_app.src.shared.tennis_game_logic import Match, GameScore


def player_won_points(tennis_match: Match, player_name: str, pts_won: int):
    for _ in range(pts_won):
        tennis_match.add_game_point(tennis_match.get_player_idx(player_name))


def player_won_games(tennis_match: Match, player_name: str, games_won: int):
    for _ in range(games_won):
        # To win a game one need 4 points
        player_won_points(tennis_match, player_name=player_name, pts_won=4)


def player_won_sets(tennis_match: Match, player_name: str, sets_won: int):
    for _ in range(sets_won):
        # To win a set one need to win 6 games
        player_won_games(tennis_match, player_name=player_name, games_won=6)


@pytest.fixture
def tennis_match():
    return Match(p1_name="P1", p2_name="P2")


@pytest.mark.parametrize(
    "player_to_win, sets_p1_won, sets_p2_won",
    [
        ("P1", 2, 0),
        ("P1", 2, 1),
        ("P2", 0, 2),
        ("P2", 1, 2),
    ],
)
def test_player_win(
    tennis_match: Match, player_to_win: str, sets_p1_won: int, sets_p2_won: int
):
    player_won_sets(
        tennis_match, player_name=tennis_match.p1_name, sets_won=sets_p1_won
    )
    player_won_sets(
        tennis_match, player_name=tennis_match.p2_name, sets_won=sets_p2_won
    )

    assert tennis_match.is_match_end() == True
    assert tennis_match.match_ended == True
    assert tennis_match.winner == player_to_win


@pytest.mark.parametrize(
    "player_to_win, sets_p1_won, sets_p2_won",
    [
        ("P1", 2, 0),
        ("P1", 2, 1),
        ("P2", 0, 2),
        ("P2", 1, 2),
    ],
)
def test_adding_pts_after_match_end_change_nothing(
    tennis_match: Match, player_to_win: str, sets_p1_won: int, sets_p2_won: int
):
    player_won_sets(
        tennis_match, player_name=tennis_match.p1_name, sets_won=sets_p1_won
    )
    player_won_sets(
        tennis_match, player_name=tennis_match.p2_name, sets_won=sets_p2_won
    )

    set_score = tennis_match.sets

    # match must be ended already, the score must not change
    player_won_sets(tennis_match, player_name=tennis_match.p1_name, sets_won=5)
    player_won_sets(tennis_match, player_name=tennis_match.p2_name, sets_won=5)

    assert tennis_match.is_match_end() is True
    assert tennis_match.match_ended is True
    assert tennis_match.winner == player_to_win
    assert set_score == tennis_match.sets


def test_to_win_set_advantage_is_needed(tennis_match: Match):
    player_won_games(tennis_match, player_name=tennis_match.p2_name, games_won=5)
    player_won_games(tennis_match, player_name=tennis_match.p1_name, games_won=6)

    assert tennis_match.is_set_end() is False

    # score is 7:5, P1 wins
    player_won_games(tennis_match, player_name=tennis_match.p1_name, games_won=1)

    assert tennis_match.p1_sets_won == 1


def test_to_win_game_advantage_is_needed(tennis_match: Match):
    # score is 40:AD
    player_won_points(tennis_match, player_name=tennis_match.p2_name, pts_won=3)
    player_won_points(tennis_match, player_name=tennis_match.p1_name, pts_won=4)

    # score is still 40:AD
    player_won_points(tennis_match, player_name=tennis_match.p2_name, pts_won=1)
    player_won_points(tennis_match, player_name=tennis_match.p1_name, pts_won=1)

    # game isn't over yet
    assert tennis_match.sets[0] == [0, 0]

    # player P1 won the game. Score is 0:0
    player_won_points(tennis_match, player_name=tennis_match.p1_name, pts_won=1)

    assert tennis_match.sets[0] == [1, 0]
    assert tennis_match.p1_game_score == 0
    assert tennis_match.p2_game_score == 0


def test_set_tiebreak_score(tennis_match: Match):
    player_won_games(tennis_match, player_name=tennis_match.p2_name, games_won=5)
    player_won_games(tennis_match, player_name=tennis_match.p1_name, games_won=6)
    player_won_games(tennis_match, player_name=tennis_match.p2_name, games_won=1)

    # score is 6:6, tiebreak game 0:0
    assert tennis_match.is_tiebreak is True

    # tiebreak 7:6, game continues
    player_won_points(tennis_match, player_name=tennis_match.p2_name, pts_won=6)
    player_won_points(tennis_match, player_name=tennis_match.p1_name, pts_won=7)

    assert tennis_match.is_tiebreak is True

    # score is 7:8, game lasts until one get advantage of two points
    player_won_points(tennis_match, player_name=tennis_match.p2_name, pts_won=2)
    assert tennis_match.is_tiebreak is True

    player_won_points(tennis_match, player_name=tennis_match.p2_name, pts_won=1)
    assert tennis_match.is_tiebreak is False
    assert tennis_match.p2_sets_won == 1


def test_get_idx_method(tennis_match: Match):
    assert tennis_match.get_player_idx("P1") == 1
    assert tennis_match.get_player_idx("P2") == 2

    with pytest.raises(ValueError):
        tennis_match.get_player_idx("Fake Player")


def test_game_score_to_str_method():
    assert Match.game_score_to_str(GameScore.LOVE) == "00"
    assert Match.game_score_to_str(GameScore.FIFTEEN) == "15"
    assert Match.game_score_to_str(GameScore.THIRTY) == "30"
    assert Match.game_score_to_str(GameScore.FOURTY) == "40"
    assert Match.game_score_to_str(GameScore.GAME_OR_AD) == "AD"

    for i in range(11):
        # 1 -> "01"
        # 2 -> "02"
        # ...
        # 10 -> "10"

        res = str(i)
        if len(res) < 2:
            res = "0" + res
        assert Match.game_score_to_str(i) == res
