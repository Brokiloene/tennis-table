import jinja2

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
        # print(template_file)
        template = cls.environment.get_template(template_file)
        return template.render(**data)
