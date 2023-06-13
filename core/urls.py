from django.views.generic import TemplateView
from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('graphics', views.GraphicsViewSet, basename='graphics')
router.register('contactformentries', views.ContactFormEntryViewSet, basename='contact-form-entries')

urlpatterns = router.urls + [
    path('createtokens/', views.MyTokenObtainPairView.as_view(), name="create-tokens"),
    path('', TemplateView.as_view(template_name='core/index.html'))
    ]
