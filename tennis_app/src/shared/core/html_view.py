from typing import Any
import jinja2

from tennis_app.src.config.settings import TEMPLATES_DIR


class HtmlView:
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR),
        autoescape=jinja2.select_autoescape(),
    )
    template_file: str = ""

    @classmethod
    def render(cls, data: dict[str, Any]) -> str:
        template = cls.environment.get_template(cls.template_file)
        return template.render(**data)
