# from selenium.common.exceptions import NoSuchElementException


from helper import *
from feedbacks_parser import get_all_feedbacks
from market_parser import parse_product

# DNS_URL = "https://www.dns-shop.ru"
# URL_EXAMPLE = "https://www.dns-shop.ru/catalog/251c82c88ed24e77/smart-chasy-i-braslety/?order=6&p=1"
# URL_EXAMPLE = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/?f[al]=4pv&p=1" # Apple
URL_EXAMPLE = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?stock=now-today-tomorrow-later&p=55"

parse_product(url=URL_EXAMPLE, pages_amount=70)
