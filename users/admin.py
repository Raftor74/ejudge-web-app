from django.contrib import admin
from .models import *


class LoginsAdmin(admin.ModelAdmin):
    list_display = ["login", "email"]
    search_fields = ["login", "email"]

    class Meta:
        model = Logins

admin.site.register(Logins, LoginsAdmin)
