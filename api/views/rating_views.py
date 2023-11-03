from datetime import datetime
from django.db.models import Avg
from rest_framework import views
from rest_framework.response import Response

from api.models import Tour, Review, TourOperator

class TourReviewAverage(views.APIView):
    """
    API view to calculate and return the mean rating for a given tour operator ID between certain dates.
    """
    def get(self, request):
        try:
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            tour_operator_id = self.request.query_params.get('tour_operator_id')
            country_id = self.request.query_params.get('country_id')
            city_id = self.request.query_params.get('city_id')
            state_id = self.request.query_params.get('state_id')

            # Convert dates to datetime.date instances
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Get the tours for the specified tour operator
            tours = Tour.objects.filter(tour_operator_id=tour_operator_id)

            if country_id:
                tours = tours.filter(country_id=country_id)
            if city_id:
                tours = tours.filter(city_id=city_id)
            if state_id:
                tours = tours.filter(state_id=state_id)

            # Get the reviews for the specified tours and date range
            reviews = Review.objects.filter(tour__in=tours, date__range=[start_date, end_date])

            # Calculate the mean rating
            mean_rating = reviews.aggregate(Avg('rating'))['rating__avg']

            if mean_rating is None:
                return Response({"detail": "No reviews found for the specified tour operator and date range."}, status=404)

            return Response({"mean_rating": mean_rating, "n_reviews": len(reviews)})

        except ValueError as e:
            return Response({"detail": "Please provide valid inputs. Error: " + str(e)}, status=400)

        except Exception as e:
            return Response({"detail": "An error occurred. Error: " + str(e)}, status=500)
