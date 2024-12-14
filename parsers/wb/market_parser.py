"""
    DOCSTRING TEMPLATE
"""
import json
import re
from pathlib import Path
import requests
from helper import *
from models import InputJSON, OutputProduct
from feedbacks_parser import get_all_feedbacks

CATALOG_URL = 'https://catalog.wb.ru/catalog/electronic22/v2/catalog'
OUTPUT_JSON = 'output.json'

def add_few_cards_to_json(file: str, data: list[dict]) -> None:
    step_print("Adding few cards to json...")
    """
        Добавляет новые карточки в файл к уже существующим.
    """
    # Проверяем, существует ли файл
    if Path(file).is_file():
        # Загружаем существующие данные из файла, если файл не пустой
        with open(file, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                # Если файл пуст или содержит некорректный JSON, начинаем с пустого списка
                existing_data = []
    else:
        existing_data = []

    # Объединяем новые данные с существующими
    existing_data.extend(data)

    # Перезаписываем файл с обновлёнными данными
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    step_print("Cards added to json!")

def get_data_from_raw_json(input_json: str):
    
    """
        Извлекает нужные данные из response json и возвращает их в виде списка словарей.
    """
    # Валидация входных данных через Pydantic
    input_data = InputJSON(**input_json)
    # Собираем данные для нового JSON
    output_products = []
    for product in input_data.data.products:
        # Используем модель для генерации выходных данных
        output_product = OutputProduct.from_product(product)
        # print(output_json)
        # exit(0)
        output_products.append(output_product.model_dump())
    # Загрузка существующих данных
    # add_data(output_json, output_products)  # Загружаем существующие данные
    # print(f"Данные успешно добавлены в JSON файл: {output_json}")
    step_print("Got all data!")
    return output_products

def parse_cards_by_url(url: str, page: int):
    """
        Парсит несколько страниц по ссылку на категорию.  <br>
        url - ссылка на категорию. <br>
        from_page - начальная страница. <br>
        pages_amount - конечная страница.
    """
    step_print("Parsing cards by url...")
    
    # Извлекает id бренда из ссылки на категорию
    def extract_fbrand_value(url: str) -> int:
        """
            Извлекает id бренда из ссылки на категорию товаров.
        """
        match = re.search(r'fbrand=(\d+)', url)
        if not match:
            raise ValueError(
                "URL не содержит параметра fbrand или он некорректен.")
        return int(match.group(1))

    params = {
        'ab_testing': 'false',
        'appType': '1',
        'curr': 'rub',
        'dest': '-1257786',
        'fbrand': str(extract_fbrand_value(url)),
        'foriginal': '1',
        'page': f"{page}",
        'sort': 'popular',
        'spp': '1',
        'subject': '515',
    }
    print(params)
    step_print("Sending responses...")
    response = requests.get(
        CATALOG_URL, params=params, timeout=10)
    few_cards = []
    step_print(f"Parsing page{page}")
    if response.status_code == 200:
        # print(f"Parsing page {params['page']} ")
        raw_data = response.json()
        step_print("Getting data from raw json...")
        few_cards += get_data_from_raw_json(raw_data)
        # add_few_cards_to_json(few_cards, output_json)
        # params['page'] = str(int(params['page']) + 1)
        response = requests.get(
            CATALOG_URL, params=params, timeout=10)
    # step_print("All responses were sent.")
    step_print("Parsing finished!")
    return few_cards

def parse_cards_by_ids(folder: str, id_list: list[int]):
    for card_id in id_list:
        feedbacks = get_all_feedbacks(product_id=card_id)
        save_log_file(f"{folder}/{card_id}_feedbacks.json", feedbacks)

# if __name__ == "__main__":
#     # BRAND_ID = 6049
#     BRAND_ID = 5772
#     SORT = "popular"
#     parse_cards_by_url(
#         f"https://www.wildberries.ru/catalog/elektronika"
#         f"/smartfony-i-telefony/vse-smartfony?sort={SORT}&fbrand={BRAND_ID}",
#         OUTPUT_JSON
#     )
