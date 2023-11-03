from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


VIATOR = 1
AIRBNB = 2
TRIPADVISOR = 3
EXPEDIA = 4
KLOOK = 5
CIVITAS = 6
GETYOURGUIDE = 7
FACEBOOK = 8
GOOGLE = 9
INSTAGRAM = 10
LINKEDIN = 11
TIQUETS = 12



STREAM_CHOICES = (
    (VIATOR, 'viator'),
    (AIRBNB, 'airbnb'),
    (TRIPADVISOR, 'tripadvisor'),
    (EXPEDIA, 'expedia'),
    (KLOOK, 'klook'),
    (CIVITAS, 'civitatis'),
    (GETYOURGUIDE, 'getyourguide'),
    (FACEBOOK, 'facebook'),
    (GOOGLE, 'google'),
    (INSTAGRAM, 'instagram'),
    (LINKEDIN, 'linkedin'),
    (TIQUETS, 'tiquets'),
)


class Review(models.Model):
    POSITIVE = 3
    NEUTRAL = 2
    NEGATIVE = 1

    SENTIMENT_CHOICES = (
        (POSITIVE, 'Positive'),
        (NEUTRAL, 'Neutral'),
        (NEGATIVE, 'Negative'),
    )

    date = models.DateField(null=True, blank=True)
    source_stream = models.PositiveSmallIntegerField(choices=STREAM_CHOICES)
    review_text = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)],null=True, blank=True)
    sentiment = models.PositiveSmallIntegerField(choices=SENTIMENT_CHOICES, null=True)
    review_url = models.TextField(null=True)
    ai_checked = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)
    product_id = models.CharField(max_length=255, null=True)
    product = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255, null=True)
    places = models.TextField(null=True)
    img = models.TextField(null=True)
    can_respond = models.BooleanField(default=False)
    tour = models.ForeignKey('Tour', related_name='reviews', on_delete=models.CASCADE, null=True)



class TourOperator(models.Model):
    name = models.CharField(max_length=1000)


class Tour(models.Model):
    NONCLASSIFIED = 0

    CATEGORIES = (
        (NONCLASSIFIED, 'Non Classified'),
    )

    date_created = models.DateTimeField(auto_now_add=True)
    tour_operator = models.ForeignKey(TourOperator, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    country_id = models.ForeignKey('api.Country', on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=100)
    city_id = models.ForeignKey('api.City', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=100, null=True)
    state_id = models.ForeignKey('api.State', on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=100, null=True)
    website = models.CharField(max_length=512)
    rating_override = models.BooleanField(default=False)
    rating = models.FloatField(default=None, null=True)
    n_reviews = models.IntegerField(default=0)
    # category = models.CharField(max_length=100)
    # category_id = models.ForeignKey('api.Category', on_delete=models.CASCADE, null=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORIES, null=False, default=NONCLASSIFIED)

    class Meta:
        ordering = ['-date_created']


class TourURL(models.Model):
    VIATOR = 1
    AIRBNB = 2
    TRIPADVISOR = 3
    EXPEDIA = 4
    KLOOK = 5
    CIVITATIS = 6
    GETYOURGUIDE = 7
    FACEBOOK = 8
    GOOGLE = 9
    INSTAGRAM = 10
    LINKEDIN = 11
    TIQUETS = 12

    STREAM_CHOICES = (
        (VIATOR, 'viator'),
        (AIRBNB, 'airbnb'),
        (TRIPADVISOR, 'tripadvisor'),
        (EXPEDIA, 'expedia'),
        (KLOOK, 'klook'),
        (CIVITATIS, 'civitatis'),
        (GETYOURGUIDE, 'getyourguide'),
        (FACEBOOK, 'facebook'),
        (GOOGLE, 'google'),
        (INSTAGRAM, 'instagram'),
        (LINKEDIN, 'linkedin'),
        (TIQUETS, 'tiquets'),
    )

    tour = models.ForeignKey(Tour, related_name='tour_urls', on_delete=models.CASCADE)
    url = models.CharField(max_length=10240)
    stream = models.IntegerField(choices=STREAM_CHOICES, default=VIATOR)
    checked = models.BooleanField(default=False)
    success = models.BooleanField(default=None, null=True)

# class Category(models.Model):
#     name = models.CharField(max_length=100)

class Country(models.Model):
    name = models.CharField(max_length=100)

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)