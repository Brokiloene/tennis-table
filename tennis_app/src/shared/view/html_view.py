import jinja2

from tennis_app.src.config.settings import TEMPLATES_DIR

class HtmlView:
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR),
        autoescape=jinja2.select_autoescape()
    )
    template = ""

    @classmethod
    def __call__(cls, data: dict):
        template_file = cls.templates[template]
        template = cls.environment.get_template(template_file)
        return template.render(**data)
