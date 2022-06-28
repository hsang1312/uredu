from urllib import response
from rest_framework import generics, status, status, exceptions
from rest_framework.response import Response

from accounts import serializers,  permissions, models
from accounts import signals
from constants import utils

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
    queryset = models.Profiles.objects.all()
    serializer_class = serializers.AccountProfileSerializer
    permission_classes = [permissions.IsAdmin]

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
