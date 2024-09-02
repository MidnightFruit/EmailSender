from django.contrib import admin

from users.models import Company


@admin.register(Company)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('email', 'company_name',)
