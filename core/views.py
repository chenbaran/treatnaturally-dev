from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Graphics, ContactFormEntry
from .serializers import MyTokenObtainPairSerializer, GraphicsSerializer, ContactFormEntrySerializer
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GraphicsViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = GraphicsSerializer
    http_method_names = ['get']
    queryset = Graphics.objects.all()


class ContactFormEntryViewSet(ModelViewSet):
    permission_classes= [AllowAny]
    serializer_class = ContactFormEntrySerializer
    http_method_names = ['post']
    queryset = ContactFormEntry.objects.all()