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

class ProductVariationInline(admin.TabularInline):
    model = models.ProductVariation
    

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['name']
    }
    actions = ['clear_stock']
    inlines = [ProductImageInline, ProductVariationInline]
    list_display = ['name', 'price',
                    'stock_status', 'categories']
    list_editable = ['price']
    list_filter = ['category', 'last_update', StockFilter]
    list_per_page = 10
    search_fields = ['name']

    def categories(self, obj):
        return ", ".join([category.title for category in obj.category.all()])

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


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['label', 'discount']
    list_editable = ['discount']
    fields = ['label', 'discount']

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
    exclude = ['billing_address', 'optional_shipping_address']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_filter = ['customer']
    list_display = ['id', 'order_name', 'final_price', 'payment_status', 'placed_at', 'customer', 'shipping_contact_details']
    fields = ['customer', 'final_price', 'payment_status', 'billing_address_details', 'optional_shipping_address_details']
    readonly_fields = ['shipping_contact_details', 'billing_address_details', 'optional_shipping_address_details']

    def order_name(self,instance):
        first_name = instance.billing_address.first_name
        last_name = instance.billing_address.last_name
        order_id = instance.id
        return format_html('<a href="/admin/store/order/{}">{} {}</a>', order_id, first_name, last_name)

    def billing_address_details(self, instance):
        first_name = instance.billing_address.first_name
        last_name = instance.billing_address.last_name
        street_address_1 = instance.billing_address.street_address_1
        street_address_2 = instance.billing_address.street_address_2
        city = instance.billing_address.city
        country = instance.billing_address.country
        zipcode = instance.billing_address.zipcode
        email = instance.billing_address.email
        phone = instance.billing_address.phone
        order_notes = instance.billing_address.order_notes
    #   return first_name + ' ' + last_name + '\n' + phone + '\n' + email + '\n' + street_address_1 + ' ' + street_address_2 + ', ' + city + ', ' + country + ', ' + zipcode + '\n' + order_notes
        return format_html('Name: {} {} <br>Contact details: <a href="mailto:{}">{}<a/> | <a href="tel:{}">{}</a> <br> Street Address 1: {}<br>Street Address 2: {}<br>City: {}<br>Country: {}<br>Zipcode: {}<br>Order notes:<br>{}', first_name, last_name, email, email, phone, phone, street_address_1, street_address_2, city, country, zipcode, order_notes)
        

    def optional_shipping_address_details(self, instance):
        if instance.optional_shipping_address:
            first_name = instance.optional_shipping_address.first_name
            last_name = instance.optional_shipping_address.last_name
            street_address_1 = instance.optional_shipping_address.street_address_1
            street_address_2 = instance.optional_shipping_address.street_address_2
            city = instance.optional_shipping_address.city
            country = instance.optional_shipping_address.country
            zipcode = instance.optional_shipping_address.zipcode
            email = instance.optional_shipping_address.email
            phone = instance.optional_shipping_address.phone
            order_notes = instance.optional_shipping_address.order_notes
        #   return first_name + ' ' + last_name + '\n' + phone + '\n' + email + '\n' + street_address_1 + ' ' + street_address_2 + ', ' + city + ', ' + country + ', ' + zipcode + '\n' + order_notes
            return format_html('Name: {} {} <br>Contact details: <a href="mailto:{}">{}<a/> | <a href="tel:{}">{}</a> <br> Street Address 1: {}<br>Street Address 2: {}<br>City: {}<br>Country: {}<br>Zipcode: {}<br>Order notes:<br>{}', first_name, last_name, email, email, phone, phone, street_address_1, street_address_2, city, country, zipcode, order_notes)
        else:
            return 'No optional shipping address was provided.'

    def shipping_contact_details(self, instance):
        email = instance.billing_address.email
        phone = instance.billing_address.phone
        return format_html('<a href="mailto:{}">{}<a/> | <a href="tel:{}">{}</a>', email, email, phone, phone)
    


@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'discount', 'expiry_date']
    fields = ['coupon_code', 'discount', 'expiry_date']
