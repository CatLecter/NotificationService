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
    FilePath,
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


class HeaderTemplateABC(BaseModel, ABC):
    field_1: str = create_abc_field("field_1")
    field_2: str = create_abc_field("field_1")
    field_3: str = create_abc_field("field_1")


class HeaderTemplate(HeaderTemplateABC):
    field_1: str = Field("MOVIE", alias="FIELD1")
    field_2: str = Field("BESTS", alias="FIELD2")
    field_3: str = Field("AUTHORS", alias="FIELD3")


class FooterTemplateABC(BaseModel, ABC):
    some_info: str = create_abc_field("some_info")
    field_1: str = create_abc_field("field_1")
    field_2: str = create_abc_field("field_2")
    field_3: str = create_abc_field("field_3")
    field_4: str = create_abc_field("field_4")


class FooterTemplate(FooterTemplateABC):
    some_info: str = Field("THANKS", alias="Some_info")
    field_1: str = Field("About us", alias="About_us")
    field_2: str = Field("News", alias="News")
    field_3: str = Field("Career", alias="Career")
    field_4: str = Field("Contact", alias="Contact")


class RegisterTemplateABC(BaseModel, ABC):
    welcome_mess: str = create_abc_field("welcome_mess")
    user_name: Union[str, EmailStr] = create_abc_field("user_name")
    message: constr(max_length=22) = create_abc_field("message")
    description: str = create_abc_field("description")


class RegisterTemplate(RegisterTemplateABC):
    welcome_mess: str = Field("WELCOME", alias="welcome")
    user_name: Union[str, EmailStr] = Field("MIKE", alias="user_name")
    message: constr(max_length=22) = Field("Some mess", alias="message")
    description: str = Field("THANKS", alias="description")


class LoginTemplateABC(BaseModel, ABC):
    login_info: constr(min_length=1, max_length=100) = create_abc_field("login_info")
    some_info: str = create_abc_field("some_info")
    add_info: str = create_abc_field("add_info")


class LoginTemplate(LoginTemplateABC):
    login_info: constr(min_length=1, max_length=100) = Field(
        "You have logged in site!", alias="login_info"
    )
    some_info: str = Field("You are some Person", alias="some_info")
    add_info: str = Field("Some date", alias="add_info")


class RegularTemplateABC(BaseModel, ABC):
    event_name: str = create_abc_field("event_name")
    event_main_info: str = create_abc_field("event_main_info")
    some_info: str = create_abc_field("some_info")
    id_info: Union[str, UUID] = create_abc_field("id_info")
    comment: str = create_abc_field("comment")
    author: str = create_abc_field("author")
    contact_face: str = create_abc_field("contact_face")


class RegularTemplate(RegularTemplateABC):
    event_name: str = Field("EVENT", alias="EVENT")
    event_main_info: str = Field("Event info" * 100, alias="event_main_info")
    some_info: str = Field("You are cool person!", alias="some_info")
    id_info: Union[str, UUID] = Field(alias="id_info", default_factory=uuid4)
    comment: str = Field("", alias="comment")
    author: str = Field("Mike", alias="from")
    contact_face: str = Field("Our Team", alias="contact_face")


class UrgentTemplateABC(BaseModel, ABC):
    event_name: str = create_abc_field("event_name")
    description: str = create_abc_field("description")
    title_event: str = create_abc_field("title_event")
    event_info: str = create_abc_field("event_info")
    red_info: Union[str, UUID] = create_abc_field("red_info")


class UrgentTemplate(UrgentTemplateABC):
    event_name: str = Field("EVENT", alias="EVENT")
    description: str = Field("THANKS " * 100, alias="description")
    title_event: str = Field("Mazafaka", alias="id_info")
    event_info: str = Field("text " * 10, alias="id_info_descript")
    red_info: Union[str, UUID] = Field(alias="red_info", default_factory=uuid4)


class HtmlTemplatesABC(BaseModel, ABC):
    base_dir: DirectoryPath = create_abc_field("base_dir")
    regis: str = create_abc_field("regis")
    header: str = create_abc_field("header")
    footer: str = create_abc_field("footer")
    login: str = create_abc_field("login")
    regular: str = create_abc_field("regular")
    urgent: str = create_abc_field("urgent")


class HtmlTemplates(HtmlTemplatesABC):
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
