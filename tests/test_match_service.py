import sys, os
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
import threading
from typing import List

from tennis_app.services.match_service.tennis_game_logic import Match
from tennis_app.services import MatchService


class TestMatch(unittest.TestCase):
    def setUp(self) -> None:
        self.match_uuid = MatchService.create_match("Player1", "Player2")
        self.change_score_cnt = 0
        self.lock = threading.Lock()
    
    def tearDown(self) -> None:
        pass

    def set_up_match(self, match_uuid, pts_win_order: List) -> None:
        for player_num in pts_win_order:
            with self.lock:
                self.change_score_cnt += int(1)
                MatchService.match_add_point(match_uuid, player_num)

    def test_no_race_on_add_match_point(self):
        pts_win_order = [1,1,1,1]*100000

        t1 = threading.Thread(target=self.set_up_match, args=(self.match_uuid, pts_win_order))
        t2 = threading.Thread(target=self.set_up_match, args=(self.match_uuid, pts_win_order))
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        match = MatchService.ongoing_matches[self.match_uuid]

        self.assertTrue(match.match_ended)
        self.assertEqual(match.winner, "Player1")
        self.assertEqual(self.change_score_cnt, 800000)


if __name__ == '__main__':
    unittest.main(verbosity=1)