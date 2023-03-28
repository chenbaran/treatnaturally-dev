from django.db import models

# Create your models here.
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator, MaxValueValidator
from django.db import models
from uuid import uuid4
from .validators import validate_file_size


class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, null=True, blank=True, default=1)
    slug = models.SlugField()
    shortDescription = models.TextField(null=True, blank=True)
    fullDescription = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    discount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        null=True, 
        blank=True)
    offerend = models.DateTimeField(blank=True, null=True)
    new = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size], null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='store/images',
        validators=[validate_file_size])


class Interest(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label

class BillingAddress(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length = 100)
    city = models.CharField(max_length=100)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=31, blank=True)
    order_notes = models.TextField(max_length=1000, blank=True)
    customer = models.OneToOneField('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.street_address_1 + ' ' + self.street_address_2 + ' ' + self.city + ', ' + self.country + ', ' + self.zipcode


class OptionalShippingAddress(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length = 100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street_address_1 = models.CharField(max_length=255, blank=True)
    street_address_2 = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=31, blank=True)
    order_notes = models.TextField(max_length=1000, blank=True, null=True)
    customer = models.OneToOneField('Customer', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.street_address_1 + ' ' + self.street_address_2 + ' ' + self.city + ', ' + self.country + ', ' + self.zipcode

class Customer(models.Model):
    MEMBERSHIP_FREE = 'Free'
    MEMBERSHIP_BRONZE = 'Bronze'
    MEMBERSHIP_SILVER = 'Silver'
    MEMBERSHIP_GOLD = 'Gold'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_FREE, 'Free'),
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    phone = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=10, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_FREE)
    interests = models.ManyToManyField(Interest, blank=True)
    billing_address = models.OneToOneField(BillingAddress, blank=True, null=True, on_delete=models.SET_NULL, related_name='customer_billing_address')
    optional_shipping_address = models.OneToOneField(OptionalShippingAddress, blank=True, null=True, on_delete=models.SET_NULL, related_name='customer_optional_shipping_address')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.billing_address and not self.billing_address.pk:
            self.billing_address.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.PROTECT)
    optional_shipping_address = models.ForeignKey(OptionalShippingAddress, blank=True, null=True, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=True, blank=True)
    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]
    def __str__(self):
        return self.billing_address.first_name + ' ' + self.billing_address.last_name + "'s order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orderitems')
    variation = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    final_price_after_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    final_price_after_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
