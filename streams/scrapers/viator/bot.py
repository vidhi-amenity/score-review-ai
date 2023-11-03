from streams.scrapers.main_bot import Mainbot
from .utils import *
import random
from api.models import Review, VIATOR
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
                print("Something went wrong with Viator Scraper")
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
        self.show_reviews()

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.sleep(2)


    def show_reviews(self):
        while True:
            time_difference = datetime.datetime.now() - self.start_process
            if time_difference > self.time_limit:
                break
            self.scrape()
            try:
                self.sleep(1)
                next_button = self.driver.find_elements('class name', "accountItem__25uw")
                next_button[-1].click()
                self.sleep(3)
            except:
                break

    def scrape(self):
        reviews = self.find_el('reviews', multiple=True)
        product = self.find_el('product').text
        for item in reviews:
            self.scroll_to_element(item)
            rating = item.find_elements('css selector',
                                          "path[d='M7.5 0a.77.77 0 00-.701.456L5.087 4.083a.785.785 0 01-.588.448l-3.827.582a.828.828 0 00-.433 1.395L3.008 9.33c.185.192.269.46.225.724l-.654 3.987a.809.809 0 00.77.958.751.751 0 00.364-.096l3.423-1.882a.752.752 0 01.728 0l3.423 1.882a.75.75 0 00.363.096.809.809 0 00.771-.958l-.654-3.987a.841.841 0 01.225-.724l2.77-2.823a.828.828 0 00-.434-1.396l-3.827-.581a.785.785 0 01-.589-.448L8.201.456A.77.77 0 007.5 0z']")

            date = item.find_element('class name', 'subtitle__3ckE').text
            product_id = item.find_element('class name', 'subtitle__3ckE').text

            button_show_more = item.find_elements('class name', 'link__WYUw')
            if button_show_more:
                button_show_more[0].click()
                self.sleep(2)
            review_text = item.find_element('xpath', './div/div[3]').text

            responded = True if item.find_elements('class name', 'response__2CvJ') else False

            review = Review.objects.filter(product_id=product_id, source_stream=VIATOR).first()

            if not review:
                Review.objects.update_or_create(
                    date=clean_date(date),
                    product_id=product_id,
                    tour=self.tour_obj,
                    defaults={
                        "product": product,
                        "rating": len(rating),
                        "review_text": clean_review(review_text),
                        "responded": responded,
                        "source_stream": VIATOR,
                        "review_url": "https://supplier.viator.com/",
                    }
                )


