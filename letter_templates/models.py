from abc import ABC
from uuid import UUID, uuid4
from os.path import exists, join
from typing import Union

from pydantic import (
    BaseModel,
    Field,
    constr,
    validator,
    EmailStr,
    DirectoryPath,
)


TEMPLATE = "./templates"
REGISTER = "register.html"
HEADER = "header.html"
FOOTER = "footer.html"
LOGIN = "login.html"
REGULAR = "regul.html"
URGENT = "ureg.html"


def create_abc_field(alias: str) -> Field:
    def default():
        raise NotImplementedError

    return Field(alias=alias, default_factory=default)


class HeaderTemplate(BaseModel):
    field_1: str = Field("MOVIE", alias="FIELD1")
    field_2: str = Field("BESTS", alias="FIELD2")
    field_3: str = Field("AUTHORS", alias="FIELD3")


class FooterTemplate(BaseModel):
    some_info: str = Field("THANKS", alias="Some_info")
    field_1: str = Field("About us", alias="About_us")
    field_2: str = Field("News", alias="News")
    field_3: str = Field("Career", alias="Career")
    field_4: str = Field("Contact", alias="Contact")


class RegisterTemplate(BaseModel):
    welcome_mess: str = Field("WELCOME", alias="welcome")
    user_name: Union[str, EmailStr] = Field("MIKE", alias="user_name")
    message: constr(max_length=22) = Field("Some mess", alias="message")
    description: str = Field("THANKS", alias="description")


class LoginTemplate(BaseModel):
    login_info: constr(min_length=1, max_length=100) = Field(
        "You have logged in site!", alias="login_info"
    )
    some_info: str = Field("You are some Person", alias="some_info")
    add_info: str = Field("Some date", alias="add_info")


class RegularTemplate(BaseModel):
    event_name: str = Field("EVENT", alias="EVENT")
    event_main_info: str = Field("Event info" * 100, alias="event_main_info")
    some_info: str = Field("You are cool person!", alias="some_info")
    id_info: Union[str, UUID] = Field(alias="id_info", default_factory=uuid4)
    comment: str = Field("", alias="comment")
    author: str = Field("Mike", alias="from")
    contact_face: str = Field("Our Team", alias="contact_face")


class UrgentTemplate(BaseModel):
    event_name: str = Field("EVENT", alias="EVENT")
    description: str = Field("THANKS " * 100, alias="description")
    title_event: str = Field("Mazafaka", alias="id_info")
    event_info: str = Field("text " * 10, alias="id_info_descript")
    red_info: Union[str, UUID] = Field(alias="red_info", default_factory=uuid4)


class HtmlTemplates(BaseModel):
    base_dir: DirectoryPath = TEMPLATE
    regis: str = REGISTER
    header: str = HEADER
    footer: str = FOOTER
    login: str = LOGIN
    regular: str = REGULAR
    urgent: str = URGENT

    @classmethod
    @validator("*")
    def dirs_must_exists(cls, value: str, values: dict):
        if isinstance(value, DirectoryPath):
            if not exists(value):
                raise ValueError
        else:
            base_dir = values["base_dir"]
            if not exists(join(base_dir, value)):
                raise ValueError
        return value
