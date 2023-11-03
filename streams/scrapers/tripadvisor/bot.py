from streams.scrapers.main_bot import Mainbot
from .utils import *
from api.models import Review, TRIPADVISOR
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
                print("Something went wrong with Tripadvisor Scraper")
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
        self.sleep(5)
        accept_button = self.wait_for_el('onetrust-accept')
        # accept_button = self.driver.find_element('id', "onetrust-accept-btn-handler")
        accept_button.click()
        self.sleep(1)
        
        # Loop to keep scraping and clicking the "Next" button
        while True:
            time_difference = datetime.datetime.now() - self.start_process
            if time_difference > self.time_limit:
                break
            self.scroll_down()
            self.scrape()
            can_continue = self.click_next()

            if not can_continue:
                break
    
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.sleep(2)


    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.sleep(1)

    def click_next(self):
        try:
            self.sleep(1)
            next_button = self.driver.find_element('class name', "xkSty")
            next_button.click()
            self.sleep(3)
            return True
        except Exception as e:
            print("Reached the last page or an error occurred.")
            return False

    def get_rating(self, review_tab):
        try:
            rating_svg = review_tab.find_element('css selector', ' div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > svg:nth-child(1)')
            rating = rating_svg.get_attribute('aria-label')
            return rating
        except Exception as e:
            rating_svg = review_tab.find_element('css selector', 'div > div > div:nth-child(2) > svg')
            rating = rating_svg.get_attribute('aria-label')
            return rating

    def scrape(self):
        self.sleep(5)
        reviews = self.find_el('reviews', multiple=True)

        last_review_elem = None
        for review_tab in reviews:
            self.scroll_to_element(review_tab)
            try:
                review_elements = review_tab.find_elements('class name','yCeTE')
                if len(review_elements) > 1:
                    review = review_elements[1].text
                    last_review_elem = review_tab
                    name = review_tab.find_elements('tag name', 'a')[1].text
                    rating = self.get_rating(review_tab)
                    date = review_tab.find_element('xpath',
                                                   './/div[contains(@class, "TreSq")]/div[contains(@class, "biGQs _P pZUbB ncFvv osNWb")]').text
                    product_id = generate_id(date+review)
                    Review.objects.update_or_create(
                        date=clean_date(date),
                        product_id=product_id,
                        tour=self.tour_obj,
                        defaults={
                            "product": name,
                            "rating": clean_rating(rating),
                            "review_text": clean_text(review),
                            "source_stream": TRIPADVISOR,
                            "review_url": self.link,
                            "img": None,
                        })
                    print('Review Processed')
                else:
                    self.scroll_to_element(last_review_elem)
                    continue
            except Exception as e:
                print(f"Error while processing a review: {e}")
                continue