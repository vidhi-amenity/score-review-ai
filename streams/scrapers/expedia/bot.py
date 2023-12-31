from .utils import *
from api.models import Review, EXPEDIA
import re
import time
import requests
from requests import Response
import logging
from copy import deepcopy
from urllib.parse import urlparse
from typing import Union
from streams.scrapers.main_bot import Mainbot
from django.conf import settings


class ScraperBot(Mainbot):
    def __init__(self, tour_url_obj, delay=2):
        self.zip_code = None
        self.address = None
        self.link = tour_url_obj.url.split('?')[0]
        self.tour_obj = tour_url_obj.tour
        self.pages = []
        self.results = []
        self.delay = delay
        self.endpoint = "https://www.expedia.com/graphql"
        self.dups = []
        self.destroy = False

        try:
            reviews = self.crawl()
            if not self.destroy:
                self.save_reviews(reviews)
                tour_url_obj.success = True
                tour_url_obj.checked = True
        except Exception as e:
            print(e)
            print("Something went wrong with GetYourGuide Scraper")
            tour_url_obj.success = False
            tour_url_obj.checked = True
        finally:
            self.close(self.results)
            tour_url_obj.save()


    def fetch(self, url, headers: dict, data: list) -> Union[Response, None]:
        try:
            if self.delay:
                time.sleep(self.delay)

            self.proxy = Mainbot.get_proxy(self)
            if not self.proxy:
                self.destroy = True
                return
            proxies = {
                "http": f"http://{self.proxy.endpoint}:{self.proxy.port}",
                "https": f"http://{self.proxy.endpoint}:{self.proxy.port}"
            }
            if settings.PRODUCTION:
                response = requests.post(url, headers=headers, json=data, proxies=proxies)
            else:
                response = requests.post(url, headers=headers, json=data)
            return response
        except Exception as e:
            print('Error during fetching the page')
            print(e)

    def parse(self, response: Response) -> list:
        reviews = []
        try:
            data = response.json()[0]['data']
            if data.get('activityReviews', {}).get('reviewsDialog', {}).get('comments', None):
                for comment in data['activityReviews']['reviewsDialog']['comments']:
                    print(f"Found review from {comment['author']}")
                    reviews.append(dict(
                        product_name=self.get_product_name(response),
                        rating=comment['overallScoreMessage']['text'],
                        date=comment['formattedSubmissionDate'],
                        review=comment['text'],
                        name=comment['author'],
                    ))
            elif data.get('propertyInfo', {}).get('reviewInfo', {}).get('reviews', None):
                for comment in data['propertyInfo']['reviewInfo']['reviews']:
                    print(f"Found review from {comment['reviewAuthorAttribution']['text']}")
                    reviews.append(dict(
                        product_name=self.get_product_name(response),
                        rating=comment['reviewScoreWithDescription']['value'],
                        date=comment['submissionTime']['longDateFormat'],
                        review=comment['text'],
                        name=comment['reviewAuthorAttribution']['text'],
                    ))

            else:
                print('No reviews found')
        except Exception as e:
            print('Error during parsing the page')
            print(e)
        finally:
            return reviews

    def get_product_name(self, response: Response) -> bytes:
        try:
            path = urlparse(response.request.headers['referer']).path
            product_name = path.split('.')[0].split('/')[-1]
            return product_name
        except Exception as e:
            print('Error during getting the product name')
            print(e)

    def crawl(self) -> list:
        headers = self.build_headers(self.link)
        page = 0
        items = []
        while True:
            payload = self.build_payload(self.link, page)
            response = self.fetch(self.endpoint, headers, payload)
            item = self.parse(response)
            if not item:
                print('Finished')
                break
            items.extend(item)
            page += 1
        return items

    def build_payload(self, url: str, page: int) -> Union[list, None]:
        try:
            _id = re.sub('[a-z]', '', re.search("\.([a-z0-9]+)", urlparse(url).path).group(1))
            if urlparse(url).query:
                payload = deepcopy(ACTIVITY_PAYLOAD)
                payload[0]['variables']['activityId'] = _id
                payload[0]['variables']['pagination']['startingIndex'] = page
            else:
                payload = deepcopy(PROPERTY_PAYLOAD)
                payload[0]['variables']['propertyId'] = _id
                payload[0]['variables']['searchCriteria']['secondary']['counts'][0]['value'] = page * 100
            return payload
        except Exception as e:
            print('Error during building the payload')
            print(e)

    def build_headers(self, url: str) -> Union[dict, None]:
        try:
            headers = deepcopy(HEADERS)
            headers['referer'] = url
            return headers
        except Exception as e:
            print('Error during building the headers')
            print(e)

    @classmethod
    def from_crawler(cls, delay=0):
        logger = logging.getLogger(__name__)
        # coloredlogs.install(level='INFO', logger=logger)
        return cls(delay, logger)

    def save_reviews(self, reviews):
        for r in reviews:
            try:

                Review.objects.update_or_create(
                    date=clean_date(r['date']),
                    product_id=generate_id(r['review'] + r['date'] + r['rating']),
                    tour=self.tour_obj,
                    defaults={
                        "rating": clean_rating(r['rating']),
                        "review_text": remove_emoji(r['review']),
                        "source_stream": EXPEDIA,
                        "review_url": self.link,
                    }
                )
            except Exception as e:
                print(e)
                pass