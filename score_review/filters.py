from django_filters import rest_framework as filters
from authentication.models import User
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Q


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email', 'name']
