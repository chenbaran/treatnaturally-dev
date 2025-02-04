---
title: Django Views for Store App
---
# Introduction

This document will walk you through the implementation of Django views for the Store App. The purpose of these views is to manage various entities such as products, categories, carts, and orders within the store application.

We will cover:

1. How the `ProductViewSet` manages product data and permissions.
2. The logic behind preventing deletion of categories and products with dependencies.
3. The handling of customer-specific actions and permissions.
4. The approach to managing cart and cart items.
5. The design of order creation and permission handling.
6. The management of user-specific billing and shipping addresses.

# Product management

<SwmSnippet path="/store/views.py" line="19">

---

The `ProductViewSet` is responsible for handling product-related operations. It uses a queryset that prefetches related images for efficiency. The view set also integrates filtering, searching, and ordering capabilities to enhance product data retrieval.

```
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'shortDescription', 'fullDescription']
    ordering_fields = ['price', 'last_update']
```

---

</SwmSnippet>

# Preventing deletion with dependencies

<SwmSnippet path="/store/views.py" line="28">

---

To maintain data integrity, the `destroy` method in both `ProductViewSet` and `CategoryViewSet` checks for dependencies before allowing deletion. For products, it ensures no order items are associated with the product. For categories, it checks for existing products within the category.

```
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
```

---

</SwmSnippet>

<SwmSnippet path="/store/views.py" line="38">

---

&nbsp;

```
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(category_id=kwargs['pk']):
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
```

---

</SwmSnippet>

# Customer-specific actions

<SwmSnippet path="/store/views.py" line="88">

---

The `CustomerViewSet` provides actions for retrieving and updating customer data. It includes custom actions like `history` and `me`, which allow customers to view their history and manage their own data, respectively. Permissions are enforced to ensure only authenticated users can access their data.

```
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')
    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            customer = request.user.customer
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'PATCH':
            print(request.data)
            customer = request.user.customer
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=customer, validated_data=serializer.validated_data)
            return Response(serializer.data)
```

---

</SwmSnippet>

# Cart and cart item management

<SwmSnippet path="/store/views.py" line="61">

---

The `CartViewSet` and `CartItemViewSet` handle operations related to shopping carts and their items. The `CartViewSet` supports creation, retrieval, and deletion of carts, while `CartItemViewSet` manages the addition, update, and removal of items within a cart.

```
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
```

---

</SwmSnippet>

<SwmSnippet path="/store/views.py" line="69">

---

&nbsp;

```
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
```

---

</SwmSnippet>

# Order creation and permissions

<SwmSnippet path="/store/views.py" line="178">

---

The `OrderViewSet` manages order-related operations. It dynamically assigns permissions based on the request method, allowing any user to create orders while restricting modifications to admin users. The `create` method uses a serializer to validate and save order data.

```
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsAdminUser()]
        elif self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
```

---

</SwmSnippet>

# User-specific billing and shipping addresses

<SwmSnippet path="/store/views.py" line="117">

---

The `BillingAddressViewSet` and `OptionalShippingAddressViewSet` allow users to manage their billing and shipping addresses. These views provide actions for retrieving, updating, and deleting addresses, with permissions ensuring only authenticated users can modify their own data.

```
class BillingAddressViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAdminUserOrPostRequest]
    serializer_class = BillingAddressSerializer
    queryset = BillingAddress.objects.all()

    @action(detail=False, methods=['GET', 'PUT', 'PATCH', 'POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        billing_address = customer.billing_address
```

---

</SwmSnippet>

<SwmSnippet path="/store/views.py" line="146">

---

&nbsp;

```
class OptionalShippingAddressViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAdminUserOrPostRequest]
    serializer_class = OptionalShippingAddressSerializer
    queryset = OptionalShippingAddress.objects.all()

    @action(detail=False, methods=['GET', 'PUT', 'PATCH', 'POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        optional_shipping_address = customer.optional_shipping_address
```

---

</SwmSnippet>

This walkthrough highlights the key design decisions and logic implemented in the Django views for the Store App, focusing on efficient data management and robust permission handling.

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBdHJlYXRuYXR1cmFsbHktZGV2JTNBJTNBY2hlbmJhcmFu" repo-name="treatnaturally-dev"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
