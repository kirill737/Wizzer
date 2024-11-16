from random import randint
from time import sleep as pause
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import re

from helper import *
from feedbacks_parser import get_feedbacks_info, get_all_feedbacks

def extract_data_from_raw_product_html(product) -> dict:
    """
        Парсит необходимую необходимые данные о товаре из куска html кода. <br>
        Возващает словарь вида: <br>
        ```
        {
            "brand": ___,
            "fullname": ___,
            "link": ___,
            "rating": ___,
            "price": ___,
            "feedbacks": ___
        }
        ```
    """
    
    def extract_fullname(product) -> str:
        fullname = product.find(
            'a', class_="catalog-product__name ui-link ui-link_black").find('span').text
        return fullname
    def extract_rating(product) -> float:
        rating = product.find('a', class_="catalog-product__rating").get("data-rating")
        return rating
    def extract_price_without_sale(product) -> int:
        raw_price = product.find('span', class_="product-buy__prev").text
        price = raw_price.replace(' ', '').replace('₽', '')
        return int(price)
    def extract_price(product) -> int:
        raw_price = product.find('div', class_='product-buy__price product-buy__price_active')
        price = raw_price.contents[0].strip().replace(' ', '').replace('₽', '')
        return int(price)
    def extract_link(product) -> str:
        feedbacks_link = product.find('a', class_="catalog-product__rating").get('href')
        return feedbacks_link
    def extract_product_id(product) -> str:
        product_id = product.get('data-entity')
        return product_id
    product_id = extract_product_id(product=product)
    feedbacks_info = get_feedbacks_info(product_id=product_id)
    json_content = {
        "brand": "Apple",
        "fullname": extract_fullname(product=product),
        "link": extract_link(product=product),
        "rating": feedbacks_info["mean"],
        "price": extract_price(product=product),
        "feedbacks": get_all_feedbacks(product_id=product_id, feedbacks_amount=feedbacks_info["amount"])
    }
    return json_content

def parse_one_page(driver, url: str) -> None:
    """
        Парсит страницу товара по ссылке.
    """
    step_print("Waiting for page to load")
    driver.get(url)
    pause(randint(7, 11))
    step_print("Start parsing page")
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # with open("parsers/dns/debug/whole.html", 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())
    products = soup.find_all('div', class_="catalog-product ui-button-widget") 
    # with open("parsers/dns/debug/oneProduct.html", 'w', encoding='utf-8') as file:
    #     file.write(products[0].prettify())
    
    parsed_phones = 0
    all_products_info_json = []
    for product in products:
        step_print(f"Parsing product {parsed_phones + 1}...")
        one_product_info_json = extract_data_from_raw_product_html(product)
        save_log_file(f"parsers/dns/debug/parts/feedbacks_phone_{parsed_phones}.json", one_product_info_json)
        step_print(f"Finish parsing this product")
        all_products_info_json.append(one_product_info_json)
        parsed_phones += 1
        # if parsed_phones > 18:
        #     break
    save_json(f"parsers/dns/result/pages/parsed_pages/page_1.json", all_products_info_json)
    step_print("End parsing page")

def check_url(string):
    # Шаблон регулярного выражения для проверки URL
    pattern = r"^https://www\.dns-shop\.ru/catalog/.+/.+/\\?order=\d+&p=\d+$"
    
    # Проверяем полное соответствие строки шаблону
    return bool(re.fullmatch(pattern, string))

def switch_page_in_url(url):
    def increment_page_num(url):
        pattern = r"(p=)(\d+)"
        def replace(match):
            current_page_num = int(match.group(2))  # извлекаем текущее значение page_num
            new_page_num = current_page_num + 1  # увеличиваем на 1
            return f"p={new_page_num}"  # возвращаем строку с новым значением

        new_page_url = re.sub(pattern, replace, url)
        return new_page_url

    first_page_pattern = r"^https://www\.dns-shop\.ru/catalog/.+/.+/$"
    any_page_pattern = r"^https://www\.dns-shop\.ru/catalog/.+/.+/\\?order=\d+&p=\d+$"

    if bool(re.fullmatch(pattern=first_page_pattern, string=url)):
        return url + "?order=6&p=2"
    elif bool(re.fullmatch(pattern=any_page_pattern, string=url)):
        return increment_page_num(url=url)


    # patern = "https://www.dns-shop.ru/catalog/*/*/"
    # patern = "https://www.dns-shop.ru/catalog/*/*/?order=6&p=1"

def parse_product(url, pages_amount=1):
    try:
        step_print("Open browser")
        driver = uc.Chrome()
        for page_number in range(1, pages_amount + 1):
            parse_one_page(driver, url=url)
            switch_page_in_url(url=url)
    finally:
        step_print("Close browser")
        # driver.quit()