from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from store.admin import ProductAdmin, ProductImageInline, ProductVariationInline
from blog.admin import BlogAdmin, BlogPostImageInline
from tags.models import TaggedItem
from store.models import Product
from blog.models import BlogPost
from ailments.models import AilmentItem
from .models import BusinessDetails, Graphics, HomePageSlider, HomePageSmallPicture, HomePageIcon, Logo, ContactFormEntry, User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )


class HomePageSliderInline(admin.TabularInline):
    model = HomePageSlider
    extra = 3
    max_num = 3

class HomePageSmallPictureInline(admin.TabularInline):
    model = HomePageSmallPicture
    extra = 3
    max_num = 3

class HomePageIconInline(admin.TabularInline):
    model = HomePageIcon
    extra = 3
    max_num = 3

class LogoInline(admin.StackedInline):
    model = Logo
    max_num = 1

class GraphicsAdmin(admin.ModelAdmin):
    inlines = [
        HomePageSliderInline,
        HomePageSmallPictureInline,
        HomePageIconInline,
        LogoInline,
    ]

    change_form_template = 'core/change_form.html'
    
    def has_delete_permission(self, request, obj=None):
      return False

    def get_urls(self):
        urls = super().get_urls()
        if not Graphics.objects.exists():
            # Create a new Graphics object
            graphics = Graphics.objects.create()
            # Redirect to the change page for the new object
            return [
                path('', lambda request: HttpResponseRedirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=[graphics.pk]))),
            ] + urls
        else:
            # Redirect to the change page for the first Graphics object
            return [
                path('', lambda request: HttpResponseRedirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=[Graphics.objects.first().pk]))),
            ] + urls

class BusinessDetailsAdmin(admin.ModelAdmin):
    change_form_template = 'core/change_form.html'
    
    def has_delete_permission(self, request, obj=None):
      return False

    def get_urls(self):
        urls = super().get_urls()
        if not BusinessDetails.objects.exists():
            # Create a new Graphics object
            businessdetails = BusinessDetails.objects.create()
            # Redirect to the change page for the new object
            return [
                path('', lambda request: HttpResponseRedirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=[businessdetails.pk]))),
            ] + urls
        else:
            # Redirect to the change page for the first Graphics object
            return [
                path('', lambda request: HttpResponseRedirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=[BusinessDetails.objects.first().pk]))),
            ] + urls

class ContactFormEntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message']
    list_per_page = 20
    search_fields = ['name__istartswith', 'email__istartswith']


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class AilmentInline(GenericTabularInline):
    autocomplete_fields = ['ailment']
    model = AilmentItem


class CustomProductAdmin(ProductAdmin):
    inlines = [ProductImageInline, ProductVariationInline, TagInline, AilmentInline]

class CustomBlogAdmin(BlogAdmin):
    inlines = [BlogPostImageInline, TagInline, AilmentInline]

admin.site.register(BusinessDetails, BusinessDetailsAdmin)
admin.site.register(Graphics, GraphicsAdmin)
admin.site.register(ContactFormEntry, ContactFormEntryAdmin)
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
admin.site.unregister(BlogPost)
admin.site.register(BlogPost, CustomBlogAdmin)


