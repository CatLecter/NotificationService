from os import listdir
from dataclasses import dataclass
from os.path import join, getmtime
from typing import Union, Optional
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel, DirectoryPath, validate_arguments, FilePath

from .models import (
    HtmlTemplates,
    FooterTemplate,
    HeaderTemplate,
    RegularTemplate,
    RegisterTemplate,
    LoginTemplate,
    UrgentTemplate,
)


TemplatesUnionType = Union[
    FooterTemplate,
    HeaderTemplate,
    RegisterTemplate,
    LoginTemplate,
    RegularTemplate,
    UrgentTemplate,
]

BodyTemplateType = Union[
    RegisterTemplate, LoginTemplate, RegularTemplate, UrgentTemplate
]


class TemplatesGetter(BaseModel):
    templates: HtmlTemplates = HtmlTemplates()

    def get_required_template_dir(self, template: TemplatesUnionType) -> str:
        if isinstance(template, FooterTemplate):
            return self.templates.footer
        elif isinstance(template, HeaderTemplate):
            return self.templates.header
        elif isinstance(template, RegisterTemplate):
            return self.templates.regis
        elif isinstance(template, LoginTemplate):
            return self.templates.login
        elif isinstance(template, RegularTemplate):
            return self.templates.regular
        elif isinstance(template, UrgentTemplate):
            return self.templates.urgent
        raise Exception(f"Template not Found {template}")

    def get_html_template(self, template: TemplatesUnionType) -> Template:
        html_file_name = self.get_required_template_dir(template)
        base_dir = self.templates.base_dir
        return self.get_required_template(base_dir=base_dir, file=html_file_name)

    @staticmethod
    @validate_arguments
    def get_html_template_file(template_dir: FilePath) -> str:
        def modification_date(filename):

            return datetime.fromtimestamp(getmtime(join(template_dir, filename)))

        files = tuple(
            (modification_date(file), file)
            for file in listdir(template_dir)
            if ".html" in file
        )
        if not files:
            raise FileNotFoundError(f"HTML file in {template_dir} not found!")

        files = sorted(files, key=lambda el: el[0])
        return files[0][-1]

    @staticmethod
    @validate_arguments
    def get_required_template(base_dir: DirectoryPath, file: str) -> Template:
        file_sys = FileSystemLoader(base_dir)
        env = Environment(loader=file_sys)
        return env.get_template(file)


@dataclass(frozen=True)
class FinalHtml:
    __slots__ = ("html_page", "header_html", "body_html", "footer_html")
    html_page: str
    header_html: str
    body_html: Optional[str]
    footer_html: Optional[str]

    def __iter__(self):
        return iter(self.html_page)

    def __str__(self):
        return self.html_page


@validate_arguments
def create_html(
    body_template: BodyTemplateType = RegularTemplate(),
    header: Optional[HeaderTemplate] = None,
    footer: Optional[FooterTemplate] = None,
) -> FinalHtml:
    template_getter = TemplatesGetter()

    def get_html(some_template: TemplatesUnionType):
        if some_template is not None:
            jinja_template = template_getter.get_html_template(some_template)
            return jinja_template.render(**some_template.dict(by_alias=True))

    header_html, body_html, footer_html = (
        get_html(header),
        get_html(body_template),
        get_html(footer),
    )

    final_html = ""
    for current_html in (header_html, body_html, footer_html):
        if current_html is not None:
            final_html += current_html

    return FinalHtml(
        html_page=final_html,
        header_html=header_html,
        body_html=body_html,
        footer_html=footer_html,
    )
