"""
    Скрипт для склеивания нескольких карточек и отзывов
"""
from helper import *
from time import sleep as pause
from feedbacks_parser import get_all_feedbacks
from market_parser import parse_brand_by_url, add_few_cards_to_json, parse_cards_by_ids

BRAND_ID = 6049  # Apple
URL = (
    "https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony"
    f"/vse-smartfony?sort=popular&fbrand={BRAND_ID}"
)

def create_few_cards(url: str, cards_amount: int) -> None:
    """
        Функция для создание json файла с несколькими товарами и отзывами на них.

        url - ссылка на страницу со всеми товарами бренда
        result_json - название конечного файла с нужное информацией
        cards_amount - кол-во товаров которое запишется в result_json
    """
    step_print("Creating few cards...")
    pages_amount = cards_amount / \
        100 if cards_amount % 100 == 0 else cards_amount / 100 + 1
    cards_data = parse_brand_by_url(url, pages_amount)
    save_json("parsers/wb/debug/1000_cards_data.json", cards_data)
    few_cards = []
    # with open(cards_json, 'r', encoding='utf-8') as cards_file:
    #     cards_data = json.load(cards_file)
    step_print("Adding feedbacks...")
    for card_num in range(cards_amount):
        # print(cards_data)
        # exit(0)
        # print(cards_data[card_num])
        product_id = cards_data[card_num]['id']
        try:
            if cards_data[card_num]['feedbacks'] > 0:
                cards_data[card_num]['feedbacks'] = get_all_feedbacks(product_id)
            else:
                []
        except:
            continue
        # print(cards_data[card_num])
        # cards_data[card_num].pop('id', None)
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
    new_cards = create_few_cards(URL, 1000)
    add_few_cards_to_json('parsers/wb/result/pages/1000_cards.json', new_cards)
