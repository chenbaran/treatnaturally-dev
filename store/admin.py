from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django import forms
from . import models


class StockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(stock__lt=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name!= '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail">')
        return ''

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['name']
    }
    actions = ['clear_stock']
    inline = [ProductImageInline]
    list_display = ['name', 'price',
                    'stock_status', 'category_title']
    list_editable = ['price']
    list_filter = ['category', 'last_update', StockFilter]
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['name']

    def category_title(self, product):
        return product.category.title

    @admin.display(ordering='stock')
    def stock_status(self, product):
        if product.stock < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear stock')
    def clear_stock(self, request, queryset):
        updated_count = queryset.update(stock=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )
    
    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, category):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, category.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )



class BillingAddressInline(admin.StackedInline):
    model = models.BillingAddress
    fields = ['first_name', 'last_name', 'country', 'city', 'street_address_1', 'street_address_2', 'zipcode', 'email', 'phone']

class OptionalShippingAddressInline(admin.StackedInline):
    model = models.OptionalShippingAddress
    fields = ['first_name', 'last_name', 'country', 'city', 'street_address_1', 'street_address_2', 'zipcode']



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ('billing_address', 'optional_shipping_address')
    list_display = ['first_name', 'last_name',  'membership', 'orders']
    list_editable = ['membership']
    inlines = [BillingAddressInline, OptionalShippingAddressInline]
    list_per_page = 10
    list_filter = ['interests']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )



@admin.register(models.Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['label']

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0

    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_filter = ['customer']
    list_display = ['id', 'placed_at', 'customer', 'shipping_address', 'shipping_contact_details']
    fields = ['customer', 'billing_address', 'optional_shipping_address', 'shipping_contact_details']
    readonly_fields = ['billing_address', 'optional_shipping_address', 'shipping_contact_details']


    def shipping_address(self, instance):
        street_address_1 = instance.billing_address.street_address_1
        street_address_2 = instance.billing_address.street_address_2
        city = instance.billing_address.city
        country = instance.billing_address.country
        return street_address_1 + ' ' + street_address_2 + ', ' + city + ', ' + country
    
    def shipping_contact_details(self, instance):
        email = instance.billing_address.email
        phone = instance.billing_address.phone
        return format_html('<a href="mailto:{}">{}<a/> | <a href="tel:{}">{}</a>', email, email, phone, phone)