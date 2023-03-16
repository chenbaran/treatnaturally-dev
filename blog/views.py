from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import BlogPost
from .serializers import BlogSerializer


# Create your views here.
class BlogViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer
    search_fields = ['title']
