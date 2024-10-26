from random import randint
from time import sleep as pause
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import requests
import json
DEBUG_MODE = 1
STEP_MODE = 1
DNS_URL = "https://www.dns-shop.ru"

def debug_print(text: str) -> None:
    if DEBUG_MODE:
        print(text)
def step_print(text: str) -> None:
    if STEP_MODE:
        print(text)

def save_log_file(path: str, content: json) -> None:
    if DEBUG_MODE:
        debug_print(f"Saving {path}")
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

def save_json(path: str, content: json) -> None:
    debug_print(f"Saving {path}")
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def extract_data_from_raw_product_html(product) -> dict:
    """
    Парсит необходимую необходимые данные о товаре из куска html кода. <br>
    Возващает словарь вида: <br>
    ```
    {
        "brand": ___,
        "fullname": ___,
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
        return price
    def extract_price(product) -> int:
        raw_price = product.find('div', class_='product-buy__price product-buy__price_active')
        price = raw_price.contents[0].strip().replace(' ', '').replace('₽', '')
        return price
    # feedbacks_link = product.find('a', class_="catalog-product__rating").get('href')
    def extract_product_id(product) -> str:
        product_id = product.get('data-entity')
        return product_id
    product_id = extract_product_id(product=product)
    feedbacks_info = get_feedbacks_info(product_id=product_id)
    json_content = {
        "brand": "Apple",
        "fullname": extract_fullname(product=product),
        "rating": feedbacks_info["mean"],
        "price": extract_price(product=product),
        "feedbacks": get_all_feedbacks(product_id=product_id, feedbacks_amount=feedbacks_info["amount"])
    }
    return json_content

def parse_one_page(driver, url: str) -> None:
    """ Парсит страницу товара по ссылке."""
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

def get_feedbacks_info(product_id: str) -> dict:
    """
    Получает информацию о кол-ве отзывов на товар и их среднюю оценку. <br>
    Возвращает словарь вида: <br>
    ```
    {
        amount: feedbacks_amount,
        mean: mean_review_value
    }
    ```
    """
    result = {}
    
    files = {
        # 'objectTypeId': (None, '610d4c8e-37fc-416c-a603-bce518d57c15'),
        'objectId': (None, product_id), 
        'isRealBuyer': (None, 'true'),
        'hasPhotos': (None, '0'),
        # 'sort': (None, '0'), # 0 - по дате
        'offset': (None, 0),
        'limit': (None, 3),
        'onlyObjectOpinions': (None, True)
    }
    feedbacks_amount = 0
    tmp_sum_value = 0
    response = requests.post('https://www.dns-shop.ru/opinion/opinions/get/', files=files)
    grades = response.json()['data']['filtersCounts'] ['grades']
    for key, value in grades.items():
        feedbacks_amount += value
        tmp_sum_value += value * int(key)
    result["amount"] = feedbacks_amount
    result["mean"] = round(tmp_sum_value / feedbacks_amount, 3)
    debug_print(f"Feedbacks info: {result}")
    return result

def get_feedbacks_part(product_id: str, offset: int, limit: int) -> list:
    """
    Получает часть отзывов на опредеённый товар, так как API не позволяет взять сразу все. <br>
    Возващает список словаей вида: <br>
    ```
    {
        'plus': ___,
        'minus': ___,
        'comment': ___,
        'rating': ___,
        "name": ___
    }
    ```
    """
    # print("Getting part of all feedbacks")
    all_feedbacks = []

    files = {
        # 'objectTypeId': (None, '610d4c8e-37fc-416c-a603-bce518d57c15'),
        'objectId': (None, product_id), 
        'isRealBuyer': (None, 'true'),
        'hasPhotos': (None, '0'),
        'sort': (None, '0'), # 0 - по дате
        'offset': (None, offset),
        'limit': (None, limit),
        'onlyObjectOpinions': (None, True)
    }

    response = requests.post('https://www.dns-shop.ru/opinion/opinions/get/', files=files)
    # Запись дебаг файла с ответом api
    if offset == 0:
        save_log_file(f"parsers/dns/debug/responses/response_{product_id}.json", response.json())
    # with open('parsers/dns/debug/test.json', 'w', encoding='utf-8') as file:
    #     json.dump(response.json(), file, ensure_ascii=False, indent=4)
    
    opinions = response.json()['data']['opinions'] 
    
    for opinion in opinions:
        # save_log_file("parsers/dns/debug/parts/lastOpinion.json", opinion)
        # save_log_file("parsers/dns/debug/parts/opinoins.json", opinions)
        all_feedbacks.append({
            'plus': opinion['plus'],
            'minus': opinion['minus'],
            'comment': opinion['comment'],
            'rating': opinion['rating'],
            "name": opinion['user']['name']
        })
    return all_feedbacks

def get_all_feedbacks(product_id: str, feedbacks_amount: int):
    """
    Получает список всех отзывов на определённый товар
    """
    step_print("Start getting all feedbacks")
    offset = 0
    limit = 10
    all_feedbacks = []
    # Пока не вернётся пустой список отзывов
    while feedbacks_amount > offset:
        part_of_feedbacks = get_feedbacks_part(product_id, offset, limit)
        
        if not part_of_feedbacks:
            break
        all_feedbacks += part_of_feedbacks
        if offset % 100 == 0:
            debug_print(f"offset: {offset} parts: {len(part_of_feedbacks)}, all: {len(all_feedbacks)}")
        offset += 10
    step_print("End getting all feedbacks")
    return all_feedbacks

try:
    step_print("Open browser")
    driver = uc.Chrome()
    parse_one_page(
        driver, "https://www.dns-shop.ru/catalog/17a8a01d16404e77/?f[al]=4pv&p=1")
finally:
    step_print("Close browser")
    # driver.quit()
