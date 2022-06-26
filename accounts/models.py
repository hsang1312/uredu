from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        
        if email is None:
            raise TypeError('Users should have a Email')
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        
        return user
        
    def create_superuser(self, email, password=None):
                
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        return user
                   
class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True, db_index=True)
    fullname = models.CharField(max_length=255, null=True)
    role = models.ForeignKey('Roles', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['role']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return  self.email
    
    def tokens(self):
        return ''

class Profiles(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=150, null=True)
    fullname = models.CharField(max_length=255, null=True)
    role = models.IntegerField(null=True)
    avatar_image = models.ImageField(null=True, blank=True, upload_to='', default=None)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, db_index=True)
    
    class Meta:
        db_table = 'profiles'
        
    def __str__(self):
        return str(self.user.email)
    
class Roles(models.Model):
    name = models.CharField(null=True , blank=True, max_length=50, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        
    def __str__(self):
        return str(self.name)
