from django.views.generic import TemplateView
from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('createtoken', views.TokenObtainPairView, basename='create-tokens')

urlpatterns = [
    path('createtokens/', views.MyTokenObtainPairView.as_view(), name="create-tokens"),
    path('', TemplateView.as_view(template_name='core/index.html'))
]