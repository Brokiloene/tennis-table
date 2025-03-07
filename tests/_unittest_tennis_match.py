import sys, os

testdir = os.path.dirname(__file__)
srcdir = ".."
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from typing import List

from tennis_app.src.shared.tennis_game_logic import Match


class TestMatch(unittest.TestCase):
    def setUp(self) -> None:
        self.match = Match("Player1", "Player2")

    def tearDown(self) -> None:
        pass

    def set_up_match(self, pts_win_order: List) -> None:
        for player_num in pts_win_order:
            self.match.add_game_point(player_num)

    def test_set_score_2_0_is_p1_win(self):
        pts_win_order = [1, 1, 1, 1] * 6 + [1, 1, 1, 1] * 6
        self.set_up_match(pts_win_order)

        self.assertTrue(self.match.match_ended)
        self.assertEqual(self.match.winner, "Player1")

    def test_set_score_2_1_is_p1_win(self):
        pts_win_order = [1, 1, 1, 1] * 6 + [2, 2, 2, 2] * 6 + [1, 1, 1, 1] * 6
        self.set_up_match(pts_win_order)

        self.assertTrue(self.match.match_ended)
        self.assertEqual(self.match.winner, "Player1")
        self.assertEqual(self.match.p2_sets_won, 1)

    def test_set_score_1_2_is_p2_win(self):
        pts_win_order = [1, 1, 1, 1] * 6 + [2, 2, 2, 2] * 6 + [2, 2, 2, 2] * 6
        self.set_up_match(pts_win_order)

        self.assertTrue(self.match.match_ended)
        self.assertEqual(self.match.winner, "Player2")
        self.assertEqual(self.match.p1_sets_won, 1)

    def test_adding_pts_after_match_end_change_nothing(self):
        pts_win_order = [1, 1, 1, 1] * 6 + [1, 1, 1, 1] * 6 + [1, 1, 1, 1] * 6
        self.set_up_match(pts_win_order)

        self.assertTrue(self.match.match_ended)
        self.assertEqual(self.match.winner, "Player1")
        self.assertEqual(self.match.p1_sets_won, 2)

    def test_to_win_set_two_game_advantage_is_needed(self):
        pts_win_order = [1, 1, 1, 1] * 5 + [2, 2, 2, 2] * 6
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.p1_sets_won, 0)
        self.assertEqual(self.match.p2_sets_won, 0)

    def test_tiebreak_on_6_6_score(self):
        pts_win_order = [1, 1, 1, 1] * 5 + [2, 2, 2, 2] * 6 + [1, 1, 1, 1]
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.p1_sets_won, 0)
        self.assertEqual(self.match.p2_sets_won, 0)
        self.assertTrue(self.match.is_tiebreak)

    def test_tiebreak_set_requires_7_pts_with_advantage_to_win(self):
        pts_win_order = [1, 1, 1, 1] * 5 + [2, 2, 2, 2] * 6 + [1, 1, 1, 1]
        pts_win_order += [1] * 5 + [2] * 7
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.p1_sets_won, 0)
        self.assertEqual(self.match.p2_sets_won, 1)
        self.assertEqual(self.match.sets[0][0], 6)
        self.assertEqual(self.match.sets[0][1], 7)
        self.assertFalse(self.match.is_tiebreak)

    def test_tiebreak_can_last_longer_if_nobody_has_advantage(self):
        pts_win_order = [1, 1, 1, 1] * 5 + [2, 2, 2, 2] * 6 + [1, 1, 1, 1]
        pts_win_order += [1] * 6 + [2] * 7 + [1, 2] * 10
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.p1_sets_won, 0)
        self.assertEqual(self.match.p2_sets_won, 0)
        self.assertTrue(self.match.is_tiebreak)

    def test_to_win_game_two_pts_advantage_is_needed(self):
        pts_win_order = [1, 1, 2, 2, 2, 2]
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.sets[0][0], 0)
        self.assertEqual(self.match.sets[0][1], 1)

    def test_when_game_ad_player_needs_to_score_two_pts_in_row_to_win(self):
        pts_win_order = [1, 1, 1, 2, 2, 2, 2, 2]
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.sets[0][0], 0)
        self.assertEqual(self.match.sets[0][1], 1)

    def test_game_ad_may_last_longer_if_nobody_get_two_pts_in_row(self):
        pts_win_order = [1, 1, 1, 2, 2, 2, 1, 2] + [1, 2] * 10
        self.set_up_match(pts_win_order)

        self.assertEqual(self.match.sets[0][0], 0)
        self.assertEqual(self.match.sets[0][1], 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
