from django.core.management.base import BaseCommand
from api.models import TourURL
from score_review.tasks import scrape


class Command(BaseCommand):
    help = 'Scrape TourURLs'

    def add_arguments(self, parser):
        help_ = """
    ID of the stream:
    VIATOR = 1
    TRIPADVISOR = 3
    EXPEDIA = 4
    KLOOK = 5
    GETYOURGUIDE = 7
    GOOGLE = 9
    TIQUETS = 12
    """
        parser.add_argument('stream_id', type=int, help=help_)

    def handle(self, *args, **options):
        stream_id = options['stream_id']
        tour_urls = TourURL.objects.filter(stream=stream_id, checked=False, success=None)
        for tour_url in tour_urls:
            scrape.delay(tour_url.id)
