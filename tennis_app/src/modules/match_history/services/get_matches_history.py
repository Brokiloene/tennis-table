from math import ceil
from typing import List, Tuple

from tennis_app.src.shared.core.service import BaseService
from tennis_app.src.shared.dao import MatchDAO
from tennis_app.src.shared.dto import ReadMatchDTO
from tennis_app.src.shared.exceptions import PaginationError


class GetMatchesHistoryService(BaseService):
    @staticmethod
    def _get_matches_count(search_name: str | None) -> int:
        return MatchDAO.get_cnt_of_matches(search_name)

    @staticmethod
    def _get_all_matches(page: int, matches_on_page_cnt: int) -> List[ReadMatchDTO]:
        return MatchDAO.fetch_all(page, matches_on_page_cnt)

    @staticmethod
    def _get_matches_filtered_by_name(
        search_query: str, page: int, matches_on_page_cnt: int
    ):
        return MatchDAO.fetch_filtered(search_query, page, matches_on_page_cnt)

    @staticmethod
    def execute(
        search_name: str | None, page: int, matches_on_page_cnt: int
    ) -> Tuple[int, int, List[ReadMatchDTO]]:
        """
        :raises: PaginationError
        """
        matches_cnt = GetMatchesHistoryService._get_matches_count(search_name)

        max_page = max(ceil(matches_cnt / matches_on_page_cnt), 1)

        if matches_cnt != 0 and matches_cnt + 1 < page * matches_on_page_cnt:
            raise PaginationError

        if page < 1:
            page = 1
        elif page > max_page:
            page = max_page

        if search_name is None:
            all_matches = GetMatchesHistoryService._get_all_matches(
                page, matches_on_page_cnt
            )
        else:
            all_matches = GetMatchesHistoryService._get_matches_filtered_by_name(
                search_name, page, matches_on_page_cnt
            )
        return (page, max_page, all_matches)
