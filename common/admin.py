from django.contrib import admin
from common.models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("name", "presence")
