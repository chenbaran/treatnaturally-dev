---
title: Django Databse Models for Store app
---
# Introduction

This document will walk you through the Django database models for the Store app. The purpose of these models is to define the structure of the database tables and their relationships, which are essential for managing store data such as products, orders, customers, and more.

We will cover:

1. How categories and products are structured and related.
2. The design of product variations and images.
3. The handling of customer information and addresses.
4. The order and cart management system.
5. The implementation of reviews and coupons.

# Category and product structure

<SwmSnippet path="/store/models.py" line="12">

---

The <SwmToken path="/store/models.py" pos="12:2:2" line-data="class Category(models.Model):">`Category`</SwmToken> model is designed to organize products into groups. It includes a title and an optional featured product, which is a foreign key to the <SwmToken path="/store/models.py" pos="15:2:2" line-data="        &#39;Product&#39;, on_delete=models.SET_NULL, null=True, related_name=&#39;+&#39;, blank=True)">`Product`</SwmToken> model. This allows for easy categorization and highlighting of specific products.

```
class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title
```

---

</SwmSnippet>

<SwmSnippet path="/store/models.py" line="24">

---

The <SwmToken path="/store/models.py" pos="24:2:2" line-data="class Product(models.Model):">`Product`</SwmToken> model is central to the store, containing fields for essential product details such as name, SKU, descriptions, price, discount, and stock. It also establishes a many-to-many relationship with the <SwmToken path="/store/models.py" pos="46:1:1" line-data="        Category, related_name=&#39;products&#39;)">`Category`</SwmToken> model, allowing products to belong to multiple categories.

```
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
        max_digits=3,
        decimal_places=0,
        validators=percentage_validator,
        null=True, 
        blank=True)
    offerend = models.DateTimeField(blank=True, null=True)
    new = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(
        Category, related_name='products')
```

---

</SwmSnippet>

# Product variations and images

<SwmSnippet path="/store/models.py" line="54">

---

The <SwmToken path="/store/models.py" pos="54:2:2" line-data="class ProductVariation(models.Model):">`ProductVariation`</SwmToken> model extends the <SwmToken path="/store/models.py" pos="55:9:9" line-data="    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name=&#39;variations&#39;)">`Product`</SwmToken> model by allowing different variations of a product, such as size or color. It includes fields for quantity, type, price, discount, SKU, stock, and an image.

```
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], null=True, blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=0, validators=percentage_validator, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size], null=True, blank=True)
```

---

</SwmSnippet>

<SwmSnippet path="/store/models.py" line="68">

---

The <SwmToken path="/store/models.py" pos="68:2:2" line-data="class ProductImage(models.Model):">`ProductImage`</SwmToken> model is straightforward, linking images to products. This is crucial for displaying product images in the store.

```
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='store/images',
        validators=[validate_file_size])


class Interest(models.Model):
    label = models.CharField(max_length=255)
```

---

</SwmSnippet>

# Customer information and addresses

<SwmSnippet path="/store/models.py" line="81">

---

The <SwmToken path="/store/models.py" pos="81:2:2" line-data="class BillingAddress(models.Model):">`BillingAddress`</SwmToken> model captures the billing details of a customer, including name, address, email, and phone number. It is linked to the <SwmToken path="/store/models.py" pos="92:10:10" line-data="    customer = models.OneToOneField(&#39;Customer&#39;, on_delete=models.SET_NULL, null=True, blank=True)">`Customer`</SwmToken> model via a one-to-one relationship.

```
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
```

---

</SwmSnippet>

<SwmSnippet path="/store/models.py" line="97">

---

The <SwmToken path="/store/models.py" pos="97:2:2" line-data="class OptionalShippingAddress(models.Model):">`OptionalShippingAddress`</SwmToken> model provides flexibility for customers who wish to specify a different shipping address. It mirrors the structure of the <SwmToken path="/store/models.py" pos="81:2:2" line-data="class BillingAddress(models.Model):">`BillingAddress`</SwmToken> model but allows for blank fields.

```
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
```

---

</SwmSnippet>

# Order and cart management

<SwmSnippet path="/store/models.py" line="168">

---

The <SwmToken path="/store/models.py" pos="168:2:2" line-data="class Order(models.Model):">`Order`</SwmToken> model tracks customer orders, including payment status, customer details, and addresses. It uses a foreign key to link to the <SwmToken path="/store/models.py" pos="92:10:10" line-data="    customer = models.OneToOneField(&#39;Customer&#39;, on_delete=models.SET_NULL, null=True, blank=True)">`Customer`</SwmToken> model and includes permissions for order management.

```
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
```

---

</SwmSnippet>

<SwmSnippet path="/store/models.py" line="194">

---

The <SwmToken path="/store/models.py" pos="194:2:2" line-data="class OrderItem(models.Model):">`OrderItem`</SwmToken> model represents individual items within an order, linking products to orders and capturing details like quantity and pricing.

```
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orderitems')
    variation = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    final_price_after_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
```

---

</SwmSnippet>

<SwmSnippet path="/store/models.py" line="204">

---

The <SwmToken path="/store/models.py" pos="204:2:2" line-data="class Cart(models.Model):">`Cart`</SwmToken> and <SwmToken path="/store/models.py" pos="209:2:2" line-data="class CartItem(models.Model):">`CartItem`</SwmToken> models manage the shopping cart functionality, allowing customers to add products to their cart before purchasing. The <SwmToken path="/store/models.py" pos="209:2:2" line-data="class CartItem(models.Model):">`CartItem`</SwmToken> model ensures that each product in a cart is unique.

```
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
```

---

</SwmSnippet>

# Reviews and coupons

<SwmSnippet path="/store/models.py" line="223">

---

The <SwmToken path="/store/models.py" pos="223:2:2" line-data="class Review(models.Model):">`Review`</SwmToken> model allows customers to leave feedback on products, capturing the reviewer's name, description, and date.

```
class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
```

---

</SwmSnippet>

<SwmSnippet path="/store/models.py" line="231">

---

The <SwmToken path="/store/models.py" pos="231:2:2" line-data="class Coupon(models.Model):">`Coupon`</SwmToken> model provides a way to apply discounts to orders, with fields for the coupon code, discount percentage, and expiry date.

```
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=3, decimal_places=0, validators=percentage_validator, null=True, blank=True)
    expiry_date = models.DateField(blank=True, null=True)
```

---

</SwmSnippet>

This structure provides a comprehensive framework for managing a store's data, ensuring that all necessary information is captured and organized efficiently.

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBdHJlYXRuYXR1cmFsbHktZGV2JTNBJTNBY2hlbmJhcmFu" repo-name="treatnaturally-dev"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
