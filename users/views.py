from django.shortcuts import render
from rest_framework import viewsets
from users.serializers import UserSerializer
from users.models import User


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """ Это ViewSet для User """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        new_user = serializer.save()
        # new_user.owner = self.request.user
        new_user.save()
