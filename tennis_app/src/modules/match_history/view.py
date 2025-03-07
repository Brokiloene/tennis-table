from typing import List
from tennis_app.src.shared.core.html_view import HtmlView
from tennis_app.src.shared.dto import ReadMatchDTO, ViewMatchDTO


class MatchHistoryView(HtmlView):
    template_file = "matches.html"
    MATCHES_ON_ONE_PAGE = 2

    @staticmethod
    def get_matches_template_data(
        all_matches: List[ReadMatchDTO], cur_page: int, max_page: int
    ) -> dict[str, str | ViewMatchDTO | list[ViewMatchDTO]]:

        def get_match_view_dto(dto: ReadMatchDTO):
            score_data = dto.score.split(" ")
            return ViewMatchDTO(
                p1_name=dto.player1_name,
                p2_name=dto.player2_name,
                p1_s1=score_data[0],
                p1_s2=score_data[2],
                p1_s3=score_data[4],
                p2_s1=score_data[1],
                p2_s2=score_data[3],
                p2_s3=score_data[5],
            )

        d: dict[str, str | ViewMatchDTO | list[ViewMatchDTO]] = {}

        cur_page_str = str(cur_page)
        max_page_str = str(max_page)

        if cur_page < 10:
            cur_page_str = "0" + cur_page_str
        if max_page < 10:
            max_page_str = "0" + max_page_str

        d["cur_page_d1"] = cur_page_str[0]
        d["cur_page_d2"] = cur_page_str[1]

        d["max_page_d1"] = max_page_str[0]
        d["max_page_d2"] = max_page_str[1]

        empty_match = ViewMatchDTO(
            p1_name="NO DATA",
            p2_name="NO DATA",
            p1_s1="0",
            p1_s2="0",
            p1_s3="0",
            p2_s1="0",
            p2_s2="0",
            p2_s3="0",
        )
        d["empty_match"] = empty_match

        matches = [get_match_view_dto(dto) for dto in all_matches]
        d["matches"] = matches
        d["next_page_num"] = str(min(cur_page + 1, max_page))
        d["prev_page_num"] = str(max(cur_page - 1, 1))

        return d
