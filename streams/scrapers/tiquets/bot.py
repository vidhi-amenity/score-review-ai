from .utils import *
from api.models import Review, TIQUETS
from django.conf import settings
from streams.scrapers.main_bot import Mainbot
from score_review.tasks import scrape_delayed
import datetime

class ScraperBot(Mainbot):
    def __init__(self, tour_url_obj):
        self.zip_code = None
        self.address = None
        self.link = tour_url_obj.url
        self.tour_obj = tour_url_obj.tour
        self.pages = []
        self.results = []
        super().__init__(__file__)
        self.start_process = datetime.datetime.now()
        self.time_limit = datetime.timedelta(minutes=5)

        if not self.destroy:
            try:
                self.start()
                tour_url_obj.success = True
            except Exception as e:
                print(e)
                print("Something went wrong with Tiquets Scraper")
                tour_url_obj.success = False
            finally:
                self.close(self.results)
                tour_url_obj.checked = True
                tour_url_obj.save()
        else:
            self.close(self.results)
            scrape_delayed.delay(tour_url_obj.id)


    def start(self):
        self.driver.get(self.link)
        self.scroll_down()
        self.show_reviews()
        self.scrape()


    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.sleep(2)


    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.sleep(2)

    def show_reviews(self):
        while True:
            time_difference = datetime.datetime.now() - self.start_process
            if time_difference > self.time_limit:
                break
            try:
                show_reviews = self.wait_for_el('show_reviews')
                show_reviews.click()
                self.sleep(2)
                reviews = self.find_el('reviews', multiple=True)
                self.scroll_to_element(reviews[-1])
            except:
                break

    def scrape(self):
        self.product = self.find_el('product').text
        reviews = self.find_el('reviews', multiple=True)
        for item in reviews:
            try:
                self.scrape_item(item)
            except Exception as e:
                print(f'TIQUETS {e}')


    def scrape_item(self, item):
        self.scroll_to_element(item)    
        review_text = self.find_el('review', item).text
        date = self.find_el('date', item).text.split('•')[0]
        rating = float(self.find_el('rating', item).get_attribute('data-rating-score'))

        product_id = generate_id(date+review_text)
        Review.objects.update_or_create(
            date=clean_date(date),
            product_id=product_id,
            rating=rating,
            tour=self.tour_obj,
            defaults={
                "product": self.product,
                "review_text": clean_text(review_text),
                "source_stream": TIQUETS,
                "review_url": self.link,
            }
        )
        

