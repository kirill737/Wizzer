import json
from models import InputJSON, OutputProduct
from pydantic import ValidationError
from pathlib import Path
from typing import Optional
import re
import requests

# Функция для загрузки существующих данных из output.json и их обновления
def addData(file: str, data: list):
    # Проверяем, существует ли файл
    if Path(file).is_file():
        # Загружаем существующие данные из файла, если файл не пустой
        with open(file, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []  # Если файл пуст или содержит некорректный JSON, начинаем с пустого списка
    else:
        existing_data = []

    # Объединяем новые данные с существующими
    existing_data.extend(data)

    # Перезаписываем файл с обновлёнными данными
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

def parse_json_file(input_file: str, output_file: str):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            inputJson = json.load(f)
        parsedData = parse_json(inputJson)
        addData(output_file, parsedData)

    except ValidationError as e:
        print("Ошибка валидации данных:", e)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
# Загрузка JSON

def parse_json(inputJson):
    # Валидация входных данных через Pydantic
    input_data = InputJSON(**inputJson)
    output_file = "output.json"
    # Собираем данные для нового JSON
    output_products = []
    for product in input_data.data.products:
        # Используем модель для генерации выходных данных
        output_product = OutputProduct.from_product(product)
        output_products.append(output_product.model_dump())
    # Загрузка существующих данных
    addData(output_file, output_products)  # Загружаем существующие данные

    print(f"Данные успешно добавлены в JSON файл: {output_file}")

def parseBrand(url:str):
    def extract_fbrand_value(url: str) -> int:
        # Регулярное выражение для поиска числа после "fbrand="
        match = re.search(r'fbrand=(\d+)', url)
        
        # Если совпадение найдено, вернем число, иначе None
        if not match:
            raise ValueError("URL не содержит параметра fbrand или он некорректен.")
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
    response = requests.get('https://catalog.wb.ru/catalog/electronic22/v2/catalog', params=params)
    
    while response.status_code == 200:
        print(f"Parsing page {params['page']} ")
        rawData = response.json()
        parse_json(rawData)
        params['page'] = str(int(params['page']) + 1)
        response = requests.get('https://catalog.wb.ru/catalog/electronic22/v2/catalog', params=params)

# def parseWBFeedbacks(id: str):

if __name__ == "__main__":
    brandId = 6049
    brandId = 5772
    parseBrand(f"https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony?sort=popular&fbrand={brandId}")
    
