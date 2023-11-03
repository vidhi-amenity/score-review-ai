from dateutil import parser
import re
import datetime
import emoji

def clean_review(text):
    if text:
        string = emoji.demojize(text)
        string = re.sub(r':[a-zA-Z_]+:', '', string)
        return string
    return None


def clean_date(str_date):
    try:
        # return parser.parse(str_date, fuzzy=True).replace(day=1)
        return datetime.date.today()
    except:
        return None
