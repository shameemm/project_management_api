from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import *

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/registration/', UserRegistrationView.as_view(), name='user-registration')
]
