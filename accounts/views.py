from rest_framework import generics, status, status, exceptions, views
from rest_framework.response import Response

from accounts import serializers,  permissions, models
from accounts import signals
from constants import utils, roles
from datetime import datetime

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
            response = utils.ResponseSuccess(message='Create account successfully!', status=status.HTTP_201_CREATED)
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
            response = utils.ResponseSuccess(message='Profile have been updated successfully', status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDeActivateView(views.APIView):
    permission_classes = [permissions.IsAdmin]
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            profile = models.Profiles.objects.get(id=pk)
        except:
            response = utils.ResponseError(message='Account profile does not exist')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        account = profile.user
        if not account.is_active:
            response = utils.ResponseError(message='Account had been de-activated before')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        account.is_active = False
        account.deleted_at = datetime.now()
        profile.deleted_at = datetime.now()
        profile.save()
        account.save()
        response = utils.ResponseSuccess(message='Account profile have been de-activated successfully', status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        profile_id = request.data.get('id', '')
        try:
            profile = models.Profiles.objects.get(id=profile_id)
        except:
            response = utils.ResponseError(message='Account profile does not exist')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        account = profile.user
        if account.is_active:
            response = utils.ResponseError(message='Account has already been active')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        account.is_active = True
        account.deleted_at = None
        profile.deleted_at = None
        profile.save()
        account.save()
        response = utils.ResponseSuccess(message='Account profile have been activated successfully', status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)