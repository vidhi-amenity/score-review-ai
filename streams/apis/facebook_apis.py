import facebook
from api.models import Review, FACEBOOK, INSTAGRAM
from .utils import clean_review, clean_date
from django.conf import settings

INSTAGRAM_PAGE_ID = '17841404642226010'
FACEBOOK_PAGE_ID = '101114676263532'


def get_facebook_comments(token=None):
    if token:
        graph = facebook.GraphAPI(token)
    else:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
    comments = []
    fields = 'id,message,created_time,comments.limit(10),permalink_url'

    posts = graph.get_connections(FACEBOOK_PAGE_ID, 'posts', fields=fields)

    for p in posts['data']:
        if 'comments' in p:
            for c in p['comments']['data']:
                Review.objects.get_or_create(
                    date=clean_date(c['created_time']),
                    product_id=c['id'],
                    defaults={
                        "rating": 0,
                        "review_text": clean_review(c['message']),
                        "responded": False,
                        "source_stream": FACEBOOK,
                        "review_url": p['permalink_url'],
                        "can_respond": True
                    })

    return comments


def get_facebook_reviews(token=None,page_id=None):
    if token:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
    else:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)

    # Campi da recuperare insieme alle recensioni, incluso il testo della recensione e la relativa valutazione numerica
    fields = 'rating,reviewer,has_rating,review_text,recommendation_type,created_time,has_review,open_graph_story'
    if page_id:
        reviews = graph.get_connections(page_id, 'ratings', fields=fields)
    else:
        reviews = graph.get_connections(FACEBOOK_PAGE_ID, 'ratings', fields=fields)


    for r in reviews['data']:
        user_id = r['open_graph_story']['id']
        review_text = r['review_text'] if r['has_review'] else ''
        date = r['created_time']
        rating = r['rating'] if r['has_rating'] else 0

        Review.objects.get_or_create(
            date=clean_date(date),
            product_id=f"{date}_{user_id}",
            defaults={
                "rating": rating,
                "review_text": clean_review(review_text),
                "responded": False,
                "source_stream": FACEBOOK,
                "can_respond": False,
                "review_url": 'https://www.facebook.com/amigotoursofficial/reviews'
            })

    return reviews['data']


def get_instagram_comments(token=None,page_id=None):
    if token:
        graph = facebook.GraphAPI(token)
    else:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
    comments = []
    fields = 'id,comments.limit(10){id,text,replies,timestamp},permalink'
    if page_id:
        posts = graph.get_connections(page_id, 'media', fields=fields)
    else:
        posts = graph.get_connections(INSTAGRAM_PAGE_ID, 'media', fields=fields)

    for p in posts['data']:
        if 'comments' in p:
            for c in p['comments']['data']:
                Review.objects.get_or_create(
                    date=clean_date(c['timestamp']),
                    product_id=c['id'],
                    defaults={
                        "rating": 0,
                        "review_text": clean_review(c['text']),
                        "responded": True if 'replies' in c else False,
                        "source_stream": INSTAGRAM,
                        "review_url": p['permalink'],
                        "can_respond": True
                    })

    return comments


def reply_facebook_comment(review, message, token=None):
    if token:
        graph = facebook.GraphAPI(token)
    else:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
    graph.put_object(parent_object=review.product_id, connection_name='comments', message=message)
    review.responded = True
    review.save()


def reply_instagram_comment(review, message,token=None):
    if token:
        graph = facebook.GraphAPI(token)
    else:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
    graph.put_object(parent_object=review.product_id, connection_name='replies', message=message)
    review.responded = True
    review.save()

