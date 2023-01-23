from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin, ProductImageInline
from blog.admin import BlogAdmin, BlogPostImageInline
from tags.models import TaggedItem
from store.models import Product
from blog.models import BlogPost
from ailments.models import AilmentItem
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class AilmentInline(GenericTabularInline):
    autocomplete_fields = ['ailment']
    model = AilmentItem


class CustomProductAdmin(ProductAdmin):
    inlines = [ProductImageInline, TagInline, AilmentInline]

class CustomBlogAdmin(BlogAdmin):
    inlines = [BlogPostImageInline, TagInline, AilmentInline]



admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
admin.site.unregister(BlogPost)
admin.site.register(BlogPost, CustomBlogAdmin)


