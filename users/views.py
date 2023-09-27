from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer, RegistrationSerializer
from users.models import User


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """ Это ViewSet для User """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """

        """
        if self.action == 'create':
            print('cr')
            permission_classes = [AllowAny]
        else:
            print('ff')
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.save()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationAPIView(APIView):
    """
    Регистрации пользователя / разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
