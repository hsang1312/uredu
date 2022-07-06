"""
Serializer accounts
"""
from datetime import datetime
from rest_framework import serializers, exceptions
from accounts import models, signals
from constants import utils, res_mess, defaults
from django.conf import settings

class CreateAccountSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y'])
    address = serializers.CharField()
    phone = serializers.CharField()
    
    class Meta:
        model = models.Users
        fields = ('email', 'fullname', 'role', 'dob', 'address', 'phone')
        extra_kwargs = {
            'fullname': {'required': True },
            'role': {'required': True },
        }
        
    def validate_role(self, value):
        account_role = value
        try:
            role = models.Roles.objects.get(id=account_role)
        except models.Roles.DoesNotExist:
            raise exceptions.ValidationError(res_mess.ErrorsRoleNotFound)
        return account_role
    
    def validate_dob(self, value):
        account_dob = datetime.strftime(value, '%Y')
        date_now = datetime.strftime(datetime.now(), '%Y')
        if (int(date_now) - int(account_dob)) < defaults.AGE_REQUIRED:
            raise exceptions.ValidationError(res_mess.ErrorsDobNotValid)
        return value
        
    def create(self, validated_data):
        password_default = 'Admin@123'
        acc_email, acc_role, acc_fullname = validated_data.get('email', ''), validated_data.get('role', ''), validated_data.get('fullname', '')
        acc_dob, acc_address, acc_phone = validated_data.get('dob', ''), validated_data.get('address', ''), validated_data.get('phone', '')
        account = models.Users.objects.create_user(email=acc_email, role=acc_role, fullname=acc_fullname, password=password_default)
        
        # Adding dob, address and phone to account profile
        profile = account.profiles
        profile.dob = acc_dob
        profile.address = acc_address
        profile.phone = acc_phone
        profile.save()
        return account
    
class AccountProfileSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y'])
    
    class Meta:
        model = models.Profiles
        fields = ('id', 'email', 'fullname', 'role', 'dob', 'address', 'phone', 'updated_at', 'deleted_at')
        extra_kwargs = {
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True}
        }
    
    def validate_role(self, value):
        account_role = value
        try:
            role = models.Roles.objects.get(id=account_role.id)
        except models.Roles.DoesNotExist:
            raise exceptions.ValidationError(res_mess.ErrorsRoleNotFound)
        return account_role
    
    def validate_dob(self, value):
        account_dob = datetime.strftime(value, '%Y')
        date_now = datetime.strftime(datetime.now(), '%Y')
        if (int(date_now) - int(account_dob)) < defaults.AGE_REQUIRED:
            raise exceptions.ValidationError(res_mess.ErrorsDobNotValid)
        return value
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.role = validated_data.get('role', instance.role)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class ForgetPasswordRequestSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = models.Users
        fields = ('email',)

class CheckResetPasswordTokenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Users
        fields = ('reset_password_token', 'reset_password_expired')

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    reset_token = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, write_only=True)
    
    def validate_password(self, value):
        password = utils.password_validate(value)
        
        if password != value:
            raise serializers.ValidationError(password)
        
        return password
    
    def validate_email(self, value):
        try:
            account = models.Users.objects.get(email=value)
        except models.Users.DoesNotExist:
            raise serializers.ValidationError(res_mess.ErrorsEmailNotValid)
        
        return value    

    def validate(self, obj):
        token = obj.get('reset_token', None)
        email = obj.get('email', None)
        
        try:
            account = models.Users.objects.get(email=email, reset_password_token=token)
        except models.Users.DoesNotExist:
            raise serializers.ValidationError({res_mess.ErrorsValidation: res_mess.ErrorsEmailOrTokenNotValid})
        
        if settings.TIME_NOW > account.reset_password_expired:
            account.reset_password_token = None
            account.reset_password_expired = None
            raise serializers.ValidationError({res_mess.ErrorsValidation: res_mess.ErrorsTokenIsExpired})
        
        return obj
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.reset_password_token = None
        instance.reset_password_expired = None
        instance.save()
        return instance