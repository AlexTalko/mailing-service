from django.contrib import admin
from mailing.models import MailingSettings, MailingMessage, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'owner',)
    list_filter = ('owner',)
    search_fields = ('email', 'owner',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'message', 'owner',)
    list_filter = ('subject', 'owner',)
    search_fields = ('subject', 'owner',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'period', 'status', 'message', 'owner',)
    list_filter = ('start_time', 'end_time', 'period', 'status', 'owner',)
    search_fields = ('start_time', 'end_time', 'period', 'status', 'owner',)
