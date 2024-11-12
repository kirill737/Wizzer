"""
    DOCSTRING TEMPLATE
"""
import json
import re
from pathlib import Path
import requests
from models import InputJSON, OutputProduct

CATALOG_URL = 'https://catalog.wb.ru/catalog/electronic22/v2/catalog'
OUTPUT_JSON = 'output.json'
# Функция для загрузки существующих данных из output.json и их обновления

def add_data(file: str, data: list) -> None:
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


def parse_json(input_json: str, output_json: str) -> None:
    """
        Parsing
    """
    # Валидация входных данных через Pydantic
    input_data = InputJSON(**input_json)
    # Собираем данные для нового JSON
    output_products = []
    for product in input_data.data.products:
        # Используем модель для генерации выходных данных
        output_product = OutputProduct.from_product(product)
        output_products.append(output_product.model_dump())
    # Загрузка существующих данных
    add_data(output_json, output_products)  # Загружаем существующие данные

    print(f"Данные успешно добавлены в JSON файл: {output_json}")


def parse_brand_by_url(url: str, output_json: str, pages_amount: int = 100):
    # Извлекает id бренда из ссылки на категорию
    def extract_fbrand_value(url: str) -> int:
        # Регулярное выражение для поиска числа после "fbrand="
        match = re.search(r'fbrand=(\d+)', url)
        # Если совпадение найдено, вернем число, иначе None
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
        'page': '1',
        'sort': 'popular',
        'spp': '1',
        'subject': '515',
    }
    response = requests.get(
        CATALOG_URL, params=params, timeout=10)
    while response.status_code == 200 and int(params['page']) <= pages_amount:
        print(f"Parsing page {params['page']} ")
        raw_data = response.json()
        parse_json(raw_data, output_json)
        params['page'] = str(int(params['page']) + 1)
        response = requests.get(
            CATALOG_URL, params=params, timeout=10)


if __name__ == "__main__":
    # BRAND_ID = 6049
    BRAND_ID = 5772
    SORT = "popular"
    parse_brand_by_url(
        f"https://www.wildberries.ru/catalog/elektronika"
        f"/smartfony-i-telefony/vse-smartfony?sort={SORT}&fbrand={BRAND_ID}",
        OUTPUT_JSON
    )
