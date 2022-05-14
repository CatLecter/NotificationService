from dataclasses import dataclass
from typing import Literal

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, validate_arguments, constr


class HtmlTemplates(BaseModel):
    pass


class RegisterHeader(BaseModel):
    move_type_one: str = 'MOVIE'
    move_type_two: str = 'BESTS'
    move_type_three: str = 'AUTHORS'


class RegisterTemplate(BaseModel):
    header: RegisterHeader
    welcome_mess: str = 'HELLO'
    user_name: str = 'MILE'
    message: constr(max_length=22) = 'Some mess'
    description: str = 'Some Info'


@dataclass(frozen=True)
class TemplatesGetter:
    template_dir: str
    template_type: Literal['register', 'login', 'hf', 'regular', 'urgent']

