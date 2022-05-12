from django.contrib import admin

from .models import Events, MessageTemplate


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "notification_id",
        "created_at",
        "last_update",
        "last_notification_send",
        "source",
        "event_type",
        "content_id",
        "data_endpoint",
    )
    list_filter = (
        "event_type",
        "source",
    )
    search_fields = (
        "source",
        "notification_id",
        "last_notification_send",
        "content_id",
        "event_type",
    )
    fields = (
        "source",
        "event_type",
        "content_id",
        "data_endpoint",
    )
    ordering = ("event_type",)


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "template_type",
        "file_name",
        "created_at",
        "last_update",
    )
    search_fields = (
        "name",
        "template_type",
    )
    list_filter = ("template_type",)
    fields = (
        "name",
        "template_type",
        "file_name",
    )
    ordering = ("name",)
