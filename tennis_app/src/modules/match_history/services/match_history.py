from math import ceil
from typing import List, Tuple

from tennis_app.src.shared.dao import MatchDAO
from tennis_app.src.shared.dto import ReadMatchDTO
from tennis_app.src.shared.exceptions import PaginationError


class MatchHistoryService:
    def _get_matches_count(search_name: str) -> int:
        return MatchDAO.get_cnt_of_matches(search_name)

    def _get_all_matches(page: int, matches_on_page_cnt: int) -> List[ReadMatchDTO]:
        return MatchDAO.fetch_all(page, matches_on_page_cnt)

    def _get_matches_filtered_by_name(
        search_query: str, page: int, matches_on_page_cnt: int
    ):
        return MatchDAO.fetch_filtered(search_query, page, matches_on_page_cnt)

    def get_matches(
        search_name: str, page: int, matches_on_page_cnt: int
    ) -> Tuple[int, int, List[ReadMatchDTO]]:
        """
        :raises: PaginationError
        """
        matches_cnt = MatchHistoryService._get_matches_count(search_name)

        max_page = max(ceil(matches_cnt / matches_on_page_cnt), 1)

        if matches_cnt != 0 and matches_cnt + 1 < page * matches_on_page_cnt:
            raise PaginationError

        if page < 1:
            page = 1
        elif page > max_page:
            page = max_page

        if search_name is None:
            all_matches = MatchHistoryService._get_all_matches(
                page, matches_on_page_cnt
            )
        else:
            all_matches = MatchHistoryService._get_matches_filtered_by_name(
                search_name, page, matches_on_page_cnt
            )
        return (page, max_page, all_matches)

    def serialize(match_data: ReadMatchDTO, page: int, max_page: int):
        d = {}
        d |= match_data.asdict()

        if page < 10:
            cur_page_str = "0" + str(page)
        if max_page < 10:
            max_page_str = "0" + str(max_page)

        d["cur_page_d1"] = cur_page_str[0]
        d["cur_page_d2"] = cur_page_str[1]

        d["max_page_d1"] = max_page_str[0]
        d["max_page_d2"] = max_page_str[1]
