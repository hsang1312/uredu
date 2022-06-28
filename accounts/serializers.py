"""
Serializer accounts
"""
from datetime import datetime
from rest_framework import serializers, exceptions
from accounts import models, signals

class CreateAccountSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y'])
    address = serializers.CharField()
    phone = serializers.CharField()
    
    class Meta:
        model = models.Users
        fields = ('email', 'fullname', 'role', 'dob', 'address', 'phone')
        
    def validate_role(self, value):
        account_role = value
        try:
            role = models.Roles.objects.get(id=account_role)
        except models.Roles.DoesNotExist:
            raise exceptions.ValidationError('Role field is not a valid role')
        return account_role
    
    def validate_dob(self, value):
        age_required = 15
        account_dob = datetime.strftime(value, '%Y')
        date_now = datetime.strftime(datetime.now(), '%Y')
        if (int(date_now) - int(account_dob)) < age_required:
            raise exceptions.ValidationError(f'Date of birth must be more than {age_required}')
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
            raise exceptions.ValidationError('Role field is not a valid role')
        return account_role
    
    def validate_dob(self, value):
        age_required = 15
        account_dob = datetime.strftime(value, '%Y')
        date_now = datetime.strftime(datetime.now(), '%Y')
        if (int(date_now) - int(account_dob)) < age_required:
            raise exceptions.ValidationError(f'Date of birth must be more than {age_required}')
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
    
    # def delete(self, instance, validated_data):
    #     user = instance.user
    #     user.is_active = False
    #     instance.deleted_at = datetime.datetime.now()
    #     return instance
        