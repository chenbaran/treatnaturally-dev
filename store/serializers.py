from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .signals import order_created
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Category, ProductImage, Review, Interest, BillingAddress, OptionalShippingAddress, ProductVariation, Membership


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['sku', 'quantity', 'price', 'stock', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'shortDescription', 'fullDescription', 'slug', 'stock',
                  'price', 'price_with_tax', 'variations', 'category', 'images','new','discount']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.price * Decimal(1.1)
    
    category = serializers.SerializerMethodField(method_name='get_category_title')

    def get_category_title(self, product: Product):
        return [product.category.title]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()


    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price', 'final_price_after_discount']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    final_price_after_discount = serializers.DecimalField(required=False, allow_null=True, max_digits=6, decimal_places=2)
    variation = serializers.CharField(required=False, allow_null=True, max_length=255)

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        variation = self.validated_data['variation']
        quantity = self.validated_data['quantity']
        final_price_after_discount = self.validated_data['final_price_after_discount']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.variation = variation
            cart_item.quantity += quantity
            cart_item.final_price_after_discount = final_price_after_discount
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'variation', 'quantity', 'final_price_after_discount']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['label']


class OptionalShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionalShippingAddress
        fields = ['id', 'first_name', 'last_name', 'country', 'city', 'street_address_1', 'street_address_2', 'zipcode', 'order_notes', 'customer']
    def create(self, validated_data):
        return OptionalShippingAddress.objects.create(**validated_data)


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['id', 'first_name', 'last_name', 'country', 'city', 'street_address_1', 'street_address_2', 'zipcode', 'email', 'phone', 'order_notes', 'customer']



class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'variation', 'unit_price', 'final_price_after_discount', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'final_price', 'billing_address', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    billing_address_id = serializers.IntegerField()
    optional_shipping_address_id = serializers.IntegerField(required=False, allow_null=True)
    final_price = serializers.DecimalField(max_digits=6, decimal_places=2)


    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            
            customer_id = self.context.get('user_id')
            if customer_id:
                customer = Customer.objects.get(user_id=customer_id)
            else:
                customer = None
            
            billing_address_id = self.validated_data['billing_address_id']
            billing_address = BillingAddress.objects.get(pk=billing_address_id)

            optional_shipping_address_id = self.validated_data.get('optional_shipping_address_id')
            optional_shipping_address = None
            if optional_shipping_address_id is not None:
                optional_shipping_address = OptionalShippingAddress.objects.get(pk=optional_shipping_address_id)
            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=cart_id)

            final_price = self.validated_data['final_price']

            order = Order.objects.create(
                customer=customer,
                billing_address=billing_address,
                optional_shipping_address=optional_shipping_address,
                final_price = final_price
            )

            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    variation=item.variation,
                    unit_price=item.product.price,
                    final_price_after_discount=item.final_price_after_discount,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            order.save()
            order_created.send_robust(self.__class__, order=order)

            return order




class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'label', 'discount_percentage']

class CustomerSerializer(serializers.ModelSerializer):
    membership = MembershipSerializer()
    user_id = serializers.IntegerField(read_only=True)
    interests = InterestsSerializer(many=True)
    billing_address = BillingAddressSerializer()
    optional_shipping_address = OptionalShippingAddressSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'access', 'user', 'user_id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership', 'orders', 'billing_address', 'optional_shipping_address', 'interests',]

    access = serializers.SerializerMethodField(method_name='get_access_true', read_only=True)
    email = serializers.SerializerMethodField(method_name='get_email', read_only=True)
    first_name = serializers.SerializerMethodField(method_name='get_first_name', read_only=True)
    last_name = serializers.SerializerMethodField(method_name='get_last_name', read_only=True)
    user = serializers.SerializerMethodField(method_name='get_username', read_only=True)
    orders = serializers.SerializerMethodField(method_name='get_orders', read_only=True)

    def get_orders(self, instance):
        orders = Order.objects.filter(customer=instance)
        order_data = OrderSerializer(orders, many=True).data
        return order_data

    def get_access_true(self, customer:Customer):
        return [True]
    
    def get_email(self, customer: Customer):
        return [customer.user.email]
    
    def get_first_name(self, customer: Customer):
        return [customer.user.first_name]
    
    def get_last_name(self, customer: Customer):
        return [customer.user.last_name]
    
    def get_username(self, customer: Customer):
        return [customer.user.username]


    def update(self, instance, validated_data):
        # Get the interests data from the validated data
        interests_data = validated_data.pop('interests', None)

        # Call the superclass's update() method to update the other fields
        instance = super().update(instance, validated_data)

        # If there is interests data, update the customer's interests
        if interests_data is not None:
            # Clear the current interests of the customer
            instance.interests.clear()

            # Create new interest objects for the customer's interests
            for interest_data in interests_data:
                interest, _ = Interest.objects.get_or_create(label=interest_data['label'])
                instance.interests.add(interest)

        return instance
            
