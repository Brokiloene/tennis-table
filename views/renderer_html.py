from typing import List

import jinja2

from dto import ReadMatchDTO, ViewMatchDTO

class RendererHTML:
    templates = {
        "index": "index.html",
        "new-match": "new-match.html",
        "match-score": "match-score.html",
        "matches": "matches.html",
        "error-page": "error-page.html"
    }

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./templates"),
        autoescape=jinja2.select_autoescape()
    )

    score_data_template = {
        "name_p1": "",
        "name_p2": "",
        "p1_digit_1": "0",
        "p1_digit_2": "0",
        "p2_digit_1": "0",
        "p2_digit_2": "0",
        "cur_set_p1": "0",
        "cur_set_p2": "0",
        "set1_p1": "0",
        "set1_p2": "0",
        "set2_p1": "0",
        "set2_p2": "0",
        "set3_p1": "0",
        "set3_p2": "0"
    }

    @classmethod
    def render(cls, template_name: str, data: dict):
        template_file = cls.templates[template_name]
        template = cls.environment.get_template(template_file)
        return template.render(**data)
    
    @staticmethod
    def get_matches_template_data(
          all_matches: List[ReadMatchDTO],
          cur_page: int, 
          max_page: int
          ):
        
        def get_match_view_dto(dto: ReadMatchDTO):
            score_data = dto.score.split(' ')
            return ViewMatchDTO(
                p1_name=dto.player1_name,
                p2_name=dto.player2_name,
                p1_s1=score_data[0],
                p1_s2=score_data[2],
                p1_s3=score_data[4],
                p2_s1=score_data[1],
                p2_s2=score_data[3],
                p2_s3=score_data[5]
            )

        d = {}

        cur_page_str = str(cur_page)
        max_page_str = str(max_page)

        if cur_page < 10:
            cur_page_str = '0' + cur_page_str
        if max_page < 10:
            max_page_str = '0' + max_page_str

        d['cur_page'] = cur_page
        d['cur_page_d1'] = cur_page_str[0]
        d['cur_page_d2'] = cur_page_str[1]

        d['max_page_d1'] = max_page_str[0]
        d['max_page_d2'] = max_page_str[1]

        empty_match_res = ViewMatchDTO(
                            p1_name='NO DATA',
                            p2_name='NO DATA',
                            p1_s1='0',
                            p1_s2='0',
                            p1_s3='0',
                            p2_s1='0',
                            p2_s2='0',
                            p2_s3='0'
                        )
        d['empty_match_res'] = empty_match_res
        
        matches = [get_match_view_dto(dto) for dto in all_matches]
        d['matches'] = matches
        d['next_page_num'] = min(cur_page+1, max_page)
        d['prev_page_num'] = max(cur_page-1, 1)

        return d
