# Пакет letter_templates
___

Папка с шаблонами распологается по:
- **letter_templates/templates**

Для работы с шаблонизатором, представлен интерфейс в виде одной функции:

    def create_html(
        body_template: BodyTemplateType = UrgentTemplate(),
        header: Optional[HeaderTemplateABC] = HeaderTemplate(),
        footer: Optional[FooterTemplateABC] = None
    ) -> FinalHtml:
        template_getter = TemplatesGetter()

        def get_html(some_template: TemplatesUnionType):
            if some_template is not None:
                jinja_template = template_getter.get_html_template(some_template)
                return jinja_template.render(**some_template.dict(by_alias=True))

        header_html, body_html, footer_html = get_html(header), get_html(body_template), get_html(footer)

        final_html = ''
        for current_html in (header_html, body_html, footer_html):
            if current_html is not None:
                final_html += current_html

        return FinalHtml(
            html_page=final_html,
            header_html=header_html,
            body_html=body_html,
            footer_html=footer_html
        )


Пример использывания:

    from letter_templates.interface import create_html

    html = create_html()

Для передачи аргументов используются модели из модуля **./models.py**

Пример:

    html = create_html(
            body_template=UrgentTemplate(),
            header=HeaderTemplate(),
            footer=FooterTemplate()
    )


Подробно, какие аргуементы можно использовать, можно посмотреть по type hinting
1. BodyTemplateType = Union[
    RegisterTemplateABC,
    LoginTemplateABC,
    RegularTemplateABC,
    UrgentTemplateABC
]

Пример:

    class RegisterTemplate(RegisterTemplateABC):
        welcome_mess: str = Field('WELCOME', alias='welcome')
        user_name: Union[str, EmailStr] = Field('MIKE', alias='user_name')
        message: constr(max_length=22) = Field('Some mess', alias='message')
        description: str = Field('THANKS', alias='description')

Использывание:

    registrator = RegisterTemplate(
        welcome_mess='mess',
        user_name='user@email.ru',
        message='mess',
        description='some text'

    )

    html = create_html(
            body_template=registrator,
    )

На выходе получаем класс **FinalHtml**

Для с ним можно работать как со строкой, поэтому для сохранения можно использовать:

    with open('test.html', 'w') as f:
        f.writelines(html)
