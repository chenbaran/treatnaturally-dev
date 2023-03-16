from django.contrib import admin
from .models import Ailment


@admin.register(Ailment)
class AilmentAdmin(admin.ModelAdmin):
    search_fields = ['title']
