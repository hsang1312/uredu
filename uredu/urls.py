from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/dashboard/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls'), name='accounts'),
    path('api/v1/students/', include('students.urls'), name='students'),
]
