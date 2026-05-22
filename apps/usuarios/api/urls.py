from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import RegistroView, CurrentUserView

urlpatterns = [
    # Auth endpoints
    path('auth/registro/', RegistroView.as_view(), name='auth_registro'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='auth_logout'),
    
    # Current user
    path('me/', CurrentUserView.as_view(), name='current_user'),
]
