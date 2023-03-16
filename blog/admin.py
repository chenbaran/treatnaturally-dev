from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


class BlogPostImageInline(admin.TabularInline):
    model = models.BlogPostImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name!= '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail">')
        return ''

@admin.register(models.BlogPost)
class BlogAdmin(admin.ModelAdmin):
    inline = [BlogPostImageInline]
    list_display = ['title', 'last_update']
    list_per_page = 10
    search_fields = ['title']
