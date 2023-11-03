from selenium.webdriver.support import expected_conditions as EC
from streams.scrapers.main_bot import Mainbot
from .utils import *
from api.models import Review, GETYOURGUIDE
from django.conf import settings
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
                print("Something went wrong with GetYourGuide Scraper")
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
        self.sleep(3)
        self.get_pages()


    def get_pages(self):
        self.click_button()
        self.scroll_down()
        while True:
            time_difference = datetime.datetime.now() - self.start_process
            if time_difference > self.time_limit:
                break
            try:
                items = self.find_el('reviews',multiple=True)
                self.scroll_into_view(items[-1])
                button = self.find_el('see_more')
                button.click()
                self.sleep(4)
            except Exception as e:
                print(e)
                break

        self.scrape_products()

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_button(self):
        try:
            element = self.find_el('total_reviews')
            self.scroll_into_view(element)
            self.sleep(2)
            button = self.find_el('show_recent_reviews')
            button.click()
            recent = self.find_el('recent_reviews')
            self.sleep(2)
            recent.click()
            self.sleep(2)
        except Exception as e:
            print(e)
            pass

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.sleep(2)

    def scrape_products(self):
        print('Scraping products')
        items = self.find_el('reviews', multiple=True)
        print(len(items))

        for item in items:
            review = ''
            try:
                review = item.find_element('tag name','p').text
                print(review)
            except:
                pass
            date = item.find_elements('tag name','p')[1].text
            name =item.find_element('tag name','span').text
            rating = len(item.find_elements('class name', 'rating-star__icon--full'))
            product_id = generate_id(name+date+review)
            Review.objects.update_or_create( 
                date=clean_date(date),
                product_id=product_id,
                tour=self.tour_obj,
                defaults={
                    "product": name,
                    "rating": int(rating),
                    "review_text": clean_text(review),
                    "source_stream": GETYOURGUIDE,
                    "review_url": self.link,
                }
            )
