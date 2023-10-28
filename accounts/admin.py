from django.contrib import admin
from .models import SignupKey


class SignupKeyAdmin(admin.ModelAdmin):
    list_display = ['code', 'used', 'used_by']


admin.site.register(SignupKey, SignupKeyAdmin)
