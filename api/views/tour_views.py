from rest_framework import generics
from ..models import TourOperator, Tour
from ..serializers import TourOperatorSerializer, TourSerializer
from rest_framework.response import Response
import math
from django.utils import timezone
import datetime

class TourOperatorListCreateView(generics.ListCreateAPIView):
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer

    def list(self, request, *args, **kwargs):
        print("Create Calling.....")
        tour_operator = request.GET.get('tour_operator', '')
        rating = request.GET.get('rating', None)

        query = TourOperator.objects.all()

        if tour_operator:
            query = query.filter(name__icontains=tour_operator)

        page = self.paginate_queryset(query)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

class TourOperatorListCreateViewNoPagination(generics.ListCreateAPIView):
    pagination_class = None
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer

class TourOperatorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer

class TourList(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def list(self, request, *args, **kwargs):
        tour_operator = request.GET.get('tour_operator', '')
        tour_operator_id = request.GET.get('tour_operator_id', '')
        rating = request.GET.get('rating', None)
        country = request.GET.get('country', '')
        city = request.GET.get('city', '')
        state = request.GET.get('state', '')
        # category = request.GET.get('category', '')
        date_created = request.GET.get('date_created', None)

        query = Tour.objects.all()

        if tour_operator:
            query = query.filter(tour_operator__name__icontains=tour_operator)
        if tour_operator_id:
            query = query.filter(tour_operator_id=tour_operator_id)
        if rating:
            # GET the rating rounding up numbers.
            # For example rating=4, gets value from 3.51 to 4.50

            # lower_bound = math.floor(float(rating)) - 0.5
            # upper_bound = lower_bound + 1
            # query = query.filter(rating__gte=lower_bound, rating__lt=upper_bound)

            # Get absolute value
            # For example rating=4, gets value from 4.0 to 4.99

            lower_bound = rating
            upper_bound = int(rating) + 1
            query = query.filter(rating__gte=lower_bound, rating__lt=upper_bound)
        if country:
            query = query.filter(country__icontains=country)
        if city:
            query = query.filter(city__icontains=city)
        if state:
            query = query.filter(state__icontains=state)
        # if category:
        #     query = query.filter(category__icontains=category)
        if date_created:
            date_created = timezone.make_aware(datetime.datetime.strptime(date_created, '%Y-%m-%d'))  # Change the format according to your date format
            query = query.filter(date_created__date__gte=date_created, date_created__date__lte=date_created)

        page = self.paginate_queryset(query)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    # from django.db.models import Avg
    # tours = Tour.objects.all()
    # for t in tours:
    #     t.rating = t.reviews.aggregate(Avg('rating'))['rating__avg']
    #     t.save()


class TourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer