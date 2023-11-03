from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from authentication.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from api.serializers import (UserSerializer, 
                             UserCreateSerializer, 
                             UserUpdateSerializer)

class IsClientUser(permissions.BasePermission):
    """
    Allows access only to Client users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == User.CLIENT


class OwnRecordPermission(permissions.BasePermission):
    """
    Allow users to only see and edit their own details.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsClientUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, role=User.USER)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




class UserPasswordResetView(APIView):
    permission_classes = [IsClientUser, OwnRecordPermission]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        password = request.data.get("new_password")
        if password:
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully."}, status=200)
        else:
            return Response({"message": "New password not provided."}, status=400)
