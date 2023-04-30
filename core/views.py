from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Graphics
from .serializers import MyTokenObtainPairSerializer, GraphicsSerializer
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GraphicsViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = GraphicsSerializer
    http_method_names = ['get']
    queryset = Graphics.objects.all()