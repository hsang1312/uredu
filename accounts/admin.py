from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Users, Profiles, Roles

from .forms import UserCreationForm, UserChangeForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Users
    list_display = ['email', 'fullname', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CustomeProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'fullname', 'id', 'created_at']
    # list_filter = ['email', 'fullname']
    search_fields = ['email', 'fullname']
    ordering = ['email']

admin.site.register(Users, CustomUserAdmin)
admin.site.register(Profiles, CustomeProfileAdmin)
admin.site.register(Roles)