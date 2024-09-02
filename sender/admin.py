from django.contrib import admin

from sender.models import Sender


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'created_at', 'frequency', 'status')
