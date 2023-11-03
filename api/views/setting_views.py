# views.py
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from api.models import Country, State, City
from api.serializers import CountrySerializer, StateSerializer, CitySerializer

# class CategoryList(generics.ListAPIView):
#     serializer_class = CategorySerializer
#     pagination_class = None

#     def get_queryset(self):
#         q = self.request.query_params.get('q', '')
#         return Category.objects.filter(name__icontains=q)

class CountryList(generics.ListAPIView):
    serializer_class = CountrySerializer
    pagination_class = None

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        return Country.objects.filter(name__icontains=q)

class StateList(generics.ListAPIView):
    serializer_class = StateSerializer
    pagination_class = None

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        return State.objects.filter(name__icontains=q)

class CityList(generics.ListAPIView):
    serializer_class = CitySerializer
    pagination_class = None

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        return City.objects.filter(name__icontains=q)
