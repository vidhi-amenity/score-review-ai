from dateutil import parser
import hashlib
import emoji
import re

def clean_date(str_date):
    try:
        return parser.parse(str_date, fuzzy=True)
    except:
        return None


def generate_id(text):
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()[:20]


def clean_text(text):
    if text:
        string = emoji.demojize(text)
        string = re.sub(r':[a-zA-Z_]+:', '', string)
        return string
    return None