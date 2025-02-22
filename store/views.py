from django.shortcuts import render
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, IsAdminUserOrPostRequest, ViewCustomerHistoryPermission
from store.pagination import DefaultPagination
from .filters import ProductFilter
from .models import BillingAddress, Cart, CartItem, Category, Coupon, Customer, Interest, OptionalShippingAddress, Order, OrderItem, Product, ProductImage, Review
from .serializers import AddCartItemSerializer, BillingAddressSerializer, CartItemSerializer, CartSerializer, CategorySerializer, CouponSerializer, CreateOrderSerializer, CustomerSerializer, InterestsSerializer, OptionalShippingAddressSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'shortDescription', 'fullDescription']
    ordering_fields = ['price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(category_id=kwargs['pk']):
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')


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

        if request.method in ['GET']:
            serializer = BillingAddressSerializer(billing_address)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = BillingAddressSerializer(data=request.data, instance=billing_address)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=customer)
            return Response(serializer.data)
        elif request.method in ['POST']:
            serializer = BillingAddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=customer)
            return Response(serializer.data)
        elif request.method in ['DELETE']:
            billing_address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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

        if request.method in ['GET']:
            serializer = OptionalShippingAddressSerializer(optional_shipping_address)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = OptionalShippingAddressSerializer(optional_shipping_address, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method in ['POST']:
            serializer = OptionalShippingAddressSerializer(optional_shipping_address, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=customer)
            return Response(serializer.data)
        elif request.method in ['DELETE']:
            optional_shipping_address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    
    

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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])


class CouponViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [AllowAny]
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()


class InterestsViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [AllowAny]
    serializer_class = InterestsSerializer
    queryset = Interest.objects.all()



