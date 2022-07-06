from django.urls import path
from accounts import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from constants import roles
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        if user.profiles.role.id == roles.MANAGER:
            token['role_id'] = roles.MANAGER
        elif user.profiles.role.id == roles.STUDENT:
            token['role_id'] = roles.STUDENT
        elif user.profiles.role.id == roles.TEACHER:
            token['role_id'] = roles.TEACHER
        elif user.profiles.role.id == roles.ADMIN:
            token['role_id'] = roles.ADMIN
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login-access'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('list/', views.ListAccountProfileView.as_view(), name='list-account-profile'),
    path('create/', views.CreateAccountView.as_view(), name='account-create'),
    path('<str:pk>/profile/', views.AccountProfileDetailView.as_view(), name='account-profile'),
    path('delete/<str:pk>/', views.AccountDeActivateView.as_view(), name='account-delete'),
    path('active/', views.AccountDeActivateView.as_view(), name='account-active'),
    path('forget-password/', views.ForgetPasswordRequestView.as_view(), name='account-forget-password'),
    path('check-token-valid/', views.ResetPasswordCheckTokenView.as_view(), name='account-check-token'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='account-reset-password'),
    # path('logout/', views.LogoutVIew.as_view(), name='logout'),
]