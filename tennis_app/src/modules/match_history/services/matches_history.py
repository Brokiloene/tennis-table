from typing import List

from tennis_app.src.shared.dao import MatchDAO
from tennis_app.src.shared.dto import ReadMatchDTO


class MatchesHistoryService:
    def get_all_matches() -> List[ReadMatchDTO]:
        return MatchDAO.fetch_all()
    def get_matches_filtered_by_name(search_name: str):
        return MatchDAO.fetch_all_filtered_by_name(search_name=search_name)
    
    def serialize(match_data: ReadMatchDTO, cur_page: int, max_page: int):
        d = {}
        d |= match_data.asdict()

        if cur_page < 10:
            cur_page_str = '0' + str(cur_page)
        if max_page < 10:
            max_page_str = '0' + str(max_page)

        d['cur_page_d1'] = cur_page_str[0]
        d['cur_page_d2'] = cur_page_str[1]

        d['max_page_d1'] = max_page_str[0]
        d['max_page_d2'] = max_page_str[1]
        