from dateutil import parser
import re
import emoji
import hashlib


def clean_date(str_date):
    try:
        str_date = str_date.replace('Written', '')
        return parser.parse(str_date, fuzzy=True)
    except:
        return None


def clean_id(string):
    if string:
        return string.split('-')[1]

    return None


def clean_rating(string):
    if string:
        return float(string.split(' ')[0])
    return None


def clean_text(text):
    if text:
        string = emoji.demojize(text)
        string = re.sub(r':[a-zA-Z_]+:', '', string)
        return string
    return None


def generate_id(text):
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()[:20]
