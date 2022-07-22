from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CustomUser

from .serializers import (
    CreateCustomUserSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)

class CreateListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class ChangePasswordView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        return self.request.user


class UsersViewSet(CreateListViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        return CreateCustomUserSerializer 

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="users_me",
    )
    def me(self, request, *args, **kwargs):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        return Response(serializer.data, status.HTTP_200_OK)
