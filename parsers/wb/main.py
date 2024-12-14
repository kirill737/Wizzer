"""
    Скрипт для склеивания нескольких карточек и отзывов
"""
from helper import *
from time import sleep as pause
from feedbacks_parser import get_all_feedbacks
from market_parser import parse_cards_by_url, add_few_cards_to_json, parse_cards_by_ids
import requests
from random import randint
from tqdm import tqdm

BRAND_ID = 6049  # Apple
URL = (
    "https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony"
    f"/vse-smartfony?sort=popular&fbrand={BRAND_ID}"
)
parsed_ids = []
def create_cards_from_page(url: str, page: int) -> None:
    """
        Функция для создание json файла с несколькими товарами и отзывами на них.

        url - ссылка на страницу со всеми товарами бренда
        page - страница для парсинга
    """
    # pages_amount = cards_amount / \
    #     100 if cards_amount % 100 == 0 else cards_amount / 100 + 1

    step_print("Creating cards from page...")
    cards_data = parse_cards_by_url(url, page)
    save_json("parsers/wb/debug/test_cards_data.json", cards_data)

    step_print("Adding feedbacks...")
    few_cards = []
    with tqdm(range(len(cards_data)), desc=f"Processing cards for page {page}", colour="green") as pbar:
        for card_num in pbar:
            product_id = cards_data[card_num]['id']

            pbar.set_description(f"Card {product_id}")  # Обновляем описание прогресса
            info = {}
            print()
            # Подбираем валидную ссылку на характеристики товара
            for basket in range(10, 20):
                link = f"https://basket-{basket}.wbbasket.ru/vol{product_id//100000}/part{product_id//1000}/{product_id}/info/ru/card.json"
                response = requests.get(link, timeout=10)
                
                print(f"\rBasket: {basket}", end="")
                # pause(randint(1, 3))
                if response.status_code == 200:
                    # print(link)
                    info = response.json()
                    print(f"response: {response.status_code}")
                    save_log_file("parsers/wb/debug/last.json", info)
                    break
            
            

            # Добавляем характеристики в карточку
            step_print(f"Добавляем характеристики к карточке {product_id}")
            for option in info.get('options', []):
                print(option)
                key = option.get('name')
                value = option.get('value')
                print(f"{key}:{value}")
                if key in ['model', 'Модель', 'модель', 'Model']:
                    cards_data[card_num]['model'] = value
                elif key in ['memory', 'память', 'Память', 'Memory', 'Объем встроенной памяти (Гб)']:
                    cards_data[card_num]['memory'] = value
                elif key in ['cpu', 'Процессор', 'процессор']:
                    cards_data[card_num]['cpu'] = value

            # Заменяем число отзывов в карточке на сами отзывы
            try:
                if cards_data[card_num].get('feedbacks', []) > 0:
                    cards_data[card_num]['feedbacks'] = get_all_feedbacks(product_id)
                else:
                    print("Нет отзывов")
                    cards_data[card_num]['feedbacks'] = []
            except Exception as e:
                print(f"Error processing feedbacks for card {product_id}: {e}")
                continue

            # Сохраняем данные
            save_log_file(f"parsers/wb/debug/cards/card_{card_num}_{product_id}.json", cards_data[card_num])
            few_cards.append(cards_data[card_num])
    # add_few_cards_to_json(result_file, few_cards)
    step_print("Feedback added.")
    step_print("Cards created!")
    return few_cards
    # with open(result_json, 'w', encoding='utf-8') as result_file:
    #     json.dump(few_cards, result_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # for i in range(10):
    #     with open('./parsers/wb/debug/test.txt', 'a') as file:
    #         file.write("i\n")
    #         pause(2)
    # folder = "parsers/wb/debug/feedbacks"
    # parse_cards_by_ids(folder=folder, id_list=[260297866])

    PAGES_TO_PARSE = 15 # На каждой странице 100 карточек
    RESULT_PATH = 'parsers/wb/result/pages/1555_cards.json'
    for page in range(3, PAGES_TO_PARSE + 1):
        new_cards = create_cards_from_page(url=URL, page=page)
        print(2)
        add_few_cards_to_json(f'parsers/wb/result/pages/{PAGES_TO_PARSE}00_cards.json', new_cards)
        print(3)