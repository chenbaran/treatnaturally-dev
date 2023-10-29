from checkout import views
from django.urls import path
from .views import *


urlpatterns = [
    path('create-checkout-session/' , CreateCheckoutSession.as_view()), 
    path('stripe-webhook/' , WebHook.as_view()), 
    path('create-portal-session/', CreatePortalSession.as_view())
]