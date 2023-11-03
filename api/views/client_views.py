from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from authentication.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import (ClientSerializer, 
                             ClientCreateSerializer, 
                             ClientUpdateSerializer)
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from score_review.filters import UserFilter

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role=User.CLIENT)
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ClientUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(role=User.CLIENT)

    def list(self, request, *args, **kwargs):
        query = request.GET.get('query', '')  # Ottieni il parametro di query dalla richiesta GET

        # if query:
        #     users = User.objects.filter(
        #         Q(name__icontains=query) | Q(email__icontains=query),
        #         role=User.CLIENT
        #     ).order_by('id')  # Ordina la queryset per un campo univoco come 'id'
        # else:
        #     users = self.filter_queryset(self.get_queryset()).order_by('id')
        users = self.filter_queryset(self.get_queryset()).order_by('id')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class ClientPasswordResetView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        password = request.data.get("new_password")
        if password:
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully."}, status=200)
        else:
            return Response({"message": "New password not provided."}, status=400)


