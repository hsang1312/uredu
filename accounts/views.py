from rest_framework import generics, status, status, exceptions, views
from rest_framework.response import Response

from accounts import serializers,  permissions, models
from accounts import signals
from constants import res_mess, utils, roles
from datetime import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import secrets

# Nếu role là admin thì có quyền query hết danh sách account trong table hoặc chỉ hiện ds đang is_active = True
def getQuerysetProfiles(check, model):
    if check.role == roles.ADMIN:
        return model.objects.all()
    else:
        return model.objects.filter(deleted_at=None)
    
class CreateAccountView(generics.CreateAPIView):
    serializer_class = serializers.CreateAccountSerializer
    permission_classes = [permissions.IsAdmin]
    
    def get_queryset(self):
        return models.User.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = utils.ResponseSuccess(message=res_mess.SuccessProfileCreate, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListAccountProfileView(generics.ListAPIView):
    serializer_class = serializers.AccountProfileSerializer
    permission_classes = [permissions.IsAdmin]
    
    def get_queryset(self, *args, **kwargs):
        return getQuerysetProfiles(self.request.user, models.Profiles)

class AccountProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.Profiles.objects.all()
    serializer_class = serializers.AccountProfileSerializer
    permission_classes = [permissions.IsAdmin]
    
    def get_object(self, queryset=None):
        profile = models.Profiles.objects.get(id=self.kwargs.get('pk'))
        return profile
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = utils.ResponseSuccess(message=res_mess.SuccessProfileUpdate, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDeActivateView(views.APIView):
    permission_classes = [permissions.IsAdmin]
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            profile = models.Profiles.objects.get(id=pk)
        except:
            response = utils.ResponseError(message=res_mess.ErrorsProfileNotFound)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        account = profile.user
        if not account.is_active:
            response = utils.ResponseError(message=res_mess.ErrorsProfileHadDeactivate)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        account.is_active = False
        account.deleted_at = datetime.utcnow()
        profile.deleted_at = datetime.utcnow()
        profile.save()
        account.save()
        response = utils.ResponseSuccess(message=res_mess.SuccessProfileDeactivate, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        profile_id = request.data.get('id', '')
        try:
            profile = models.Profiles.objects.get(id=profile_id)
        except:
            response = utils.ResponseError(message=res_mess.ErrorsProfileNotFound)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        account = profile.user
        if account.is_active:
            response = utils.ResponseError(message=res_mess.ErrorsProfileIsActive)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        account.is_active = True
        account.deleted_at = None
        profile.deleted_at = None
        profile.save()
        account.save()
        response = utils.ResponseSuccess(message=res_mess.SuccessProfileActivate, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)
    
class ForgetPasswordRequestView(views.APIView):
    serializer_class = serializers.ForgetPasswordRequestSerializer
    
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email', '')
        try:
            account = models.Users.objects.get(email=email)
        except models.Users.DoesNotExist:
            response = utils.ResponseError(message=res_mess.ErrorsEmailNotValid)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)      
          
        reset_token = settings.RESET_STRING_TOKEN + secrets.token_hex(15)
        expires = settings.TIME_NOW + settings.EMAIL_RESET_TOKEN_EXPIRE_MINUTES # Default 15 minutes
        
        account.reset_password_token = reset_token
        account.reset_password_expired = expires
        account.save()
        
        reset_subject = 'FORGET PASSWORD REQUEST'
        relative_url = reverse('account-check-token')
        curent_site = get_current_site(request).domain
        absolute_url = 'http://'+curent_site+relative_url+'?token='+str(reset_token)+'&email='+str(email)
        reset_body = f'Hi please click to this link to reset your account password: {absolute_url}'

        utils.send_mail(email_receiver=email, email_subject=reset_subject, email_body=reset_body)
        
        response = utils.ResponseSuccess(message=res_mess.SuccessSendEmailForgetPassword, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)

class ResetPasswordCheckTokenView(views.APIView):
    serializer_class = serializers.CheckResetPasswordTokenSerializer
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        token = request.data.get('reset_token', None)
        try:
            account = models.Users.objects.get(email=email, reset_password_token=token)
        except:
            response = utils.ResponseError(message=res_mess.ErrorsTokenNotValidOrExpired)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if settings.TIME_NOW > account.reset_password_expired:
            account.reset_password_token = None
            account.reset_password_expired = None
            account.save()
            response = utils.ResponseError(message=res_mess.ErrorsTokenIsExpired)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = utils.ResponseSuccess(message=res_mess.SuccessTokenIsValid, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)
        
     
class ResetPasswordView(views.APIView):
    serializer_class = serializers.ResetPasswordRequestSerializer
    
    def get_object(self, request, *args, **kwargs):
        obj = models.Users.objects.get(email=request.data.get('email', None))
        return obj
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = utils.ResponseSuccess(message=res_mess.SuccessResetPassword, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)