from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from api.views import client_views, user_views,tour_views,file_views,rating_views, setting_views
router = DefaultRouter()

router.register(r'clients', client_views.ClientViewSet, basename='clients')
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('clients/<int:pk>/reset-password/', client_views.ClientPasswordResetView.as_view(), name='client-reset-password'),
    path('users/<int:pk>/reset-password/', user_views.UserPasswordResetView.as_view(), name='user-reset-password'),
    path('tour-operators/', tour_views.TourOperatorListCreateView.as_view(), name='tour-operator-list-create'),
    path('tour-operators-no-pagination/', tour_views.TourOperatorListCreateViewNoPagination.as_view(), name='tour-operator-list-create'),
    path('tour-operators/<int:pk>/', tour_views.TourOperatorRetrieveUpdateDestroyView.as_view(), name='tour-operator-retrieve-update-destroy'),
    path('tours/', tour_views.TourList.as_view()),
    path('tours/<int:pk>/', tour_views.TourDetail.as_view()),
    path('upload-tours/', file_views.FileUploadView.as_view(), name='upload-tours'),
    path('tour_review_average/', rating_views.TourReviewAverage.as_view(), name='tour-review-average'),
    path('countries/', setting_views.CountryList.as_view(), name='country-list'),
    path('states/', setting_views.StateList.as_view(), name='state-list'),
    path('cities/', setting_views.CityList.as_view(), name='city-list'),
    # path('category/', setting_views.CategoryList.as_view(), name='category-list'),
]