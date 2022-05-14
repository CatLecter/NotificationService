import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("Дата создания события"), auto_now_add=True)
    last_update = models.DateTimeField(_("Дата обновления события"), auto_now=True)

    class Meta:
        abstract = True


class EventType(models.TextChoices):
    URGENT = "URGENT", _("URGENT")
    REGULAR = "REGULAR", _("REGULAR")


class Source(models.TextChoices):
    UGC = "UGC", _("UGC")
    AUTH = "AUTH", _("AUTH")
    USER = "USER", _("USER")
    ADMIN = "ADMIN", _("ADMIN")


class ActionType(models.TextChoices):
    DELETE = "DELETE", _("DELETE")
    CREATE = "CREATE", _("CREATE")
    UPDATE = "UPDATE", _("UPDATE")
    ADD = "ADD", _("ADD")
    LOGIN = "LOGIN", _("LOGIN")
    REGISTRATION = "REGISTRATION", _("REGISTRATION")


class Events(TimeStampedModel):
    notification_id = models.UUIDField(
        _("id события"),
        default=uuid.uuid4,
        editable=False,
        blank=True,
    )
    last_notification_send = models.DateTimeField(
        _("Дата отправки уведомления"),
        null=True,
        default=None,
    )
    source = models.CharField(
        _("Сервис-источник"),
        null=False,
        max_length=20,
        choices=Source.choices,
    )
    event_type = models.CharField(
        _("Приоритет"),
        max_length=20,
        choices=EventType.choices,
    )
    content_id = models.UUIDField(_("UUID сущности"), editable=True)
    action = models.CharField(_("Действие"), max_length=20, choices=ActionType.choices)
    data_endpoint = models.URLField(
        _("Эндпоинт получения данных о сущности"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Событие")
        verbose_name_plural = _("События")
        db_table = '"public"."events"'

    def __str__(self):
        return self.notification_id


class TemplateType(models.TextChoices):
    HEADER = "header", _("HEADER")
    BODY = "body", _("BODY")
    FOOTER = "footer", _("FOOTER")


class MessageTemplate(TimeStampedModel):
    name = models.CharField(_("Имя шаблона"), max_length=255)
    template_type = models.CharField(
        _("Тип шаблона"),
        max_length=20,
        choices=TemplateType.choices,
    )
    template_file = models.FileField(
        _("Файл шаблона"),
        # upload_to="templates",
        blank=True,
        null=False,
    )

    class Meta:
        verbose_name = _("Шаблон сообщения")
        verbose_name_plural = _("Шаблоны сообщения")
        db_table = '"public"."message_templates"'

    def __str__(self):
        return self.name
