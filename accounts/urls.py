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
        if user.profiles.role == roles.MANAGER:
            token['role'] = roles.MANAGER
        elif user.profiles.role == roles.STUDENT:
            token['role'] = roles.STUDENT
        elif user.profiles.role == roles.TEACHER:
            token['role'] = roles.TEACHER
        elif user.profiles.role == roles.ADMIN:
            token['role'] = roles.ADMIN
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login-access'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    # path('logout/', views.LogoutVIew.as_view(), name='logout'),
]