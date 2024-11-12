"""
    Скрипт для склеивания нескольких карточек и отзывов
"""
import json
from feedbacks_parser import get_all_feedbacks
from market_parser import parse_brand_by_url

BRAND_ID = 6049  # Apple
URL = (
    "https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony"
    f"/vse-smartfony?sort=popular&fbrand={BRAND_ID}"
)

def create_few_cards(url: str, cards_json: str, result_json: str,  cards_amount: int) -> None:
    """
        Функция для создание json файла с несколькими товарами и отзывами на них.

        url - ссылка на страницу со всеми товарами бренда\n
        cards_json - название файла со спаршенными товарами\n
        result_json - название конечного файла с нужное информацией\n
        cards_amount - кол-во товаров которое запишется в result_json
    """
    pages_amount = cards_amount / \
        100 if cards_amount % 100 == 0 else cards_amount / 100 + 1
    parse_brand_by_url(url, cards_json, pages_amount)
    few_cards = []
    with open(cards_json, 'r', encoding='utf-8') as cards_file:
        cards_data = json.load(cards_file)
    for card_num in range(cards_amount):
        cards_data[card_num]['feedbacks'] = get_all_feedbacks(
            cards_data[card_num]['id'])
        few_cards.append(cards_data[card_num])
    with open(result_json, 'w', encoding='utf-8') as result_file:
        json.dump(few_cards, result_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    create_few_cards(URL, './parsers/wb/result/debug/iphones.json', './parsers/wb/result/pages/page_1.json', 10)
