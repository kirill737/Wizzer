# from selenium.common.exceptions import NoSuchElementException


from helper import *
from feedbacks_parser import get_all_feedbacks
from market_parser import parse_product

# DNS_URL = "https://www.dns-shop.ru"
URL_EXAMPLE = "https://www.dns-shop.ru/catalog/251c82c88ed24e77/smart-chasy-i-braslety/?order=6&p=1"
parse_product(URL_EXAMPLE)
