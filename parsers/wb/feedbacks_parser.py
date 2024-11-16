"""
    Файл для парсинга непосредственно отщзывов
"""
import requests
from helper import *
# DEBUG_MODE = 0
def get_root_by_id(product_id: int) -> int:
    """
        Находит root по id продукта.
    """
    step_print("Getting root...")
    response = requests.get(
        f"https://card.wb.ru/cards/v2/detail?"
        f"appType=1&curr=rub&dest=-1257786&nm={product_id}",
        timeout=10
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Wrong response code: {response.status_code}"
        )
    root_json = response.json()
    try:
        root_value = root_json['data']['products'][0]['root']
        return root_value
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Json access error") from exc

def get_raw_feedbacks_by_root_index(root: int, index: int) -> dict:
    step_print(f"Getting raw feedbacks by root {root}...")
    response = requests.get(
        f"https://feedbacks{index}.wb.ru/feedbacks/v2/{root}",
        timeout=10
    )
    step_print("Got response")
    if response.status_code != 200:
        raise RuntimeError(
            f"Wrong response code: {response.status_code}"
        )
    feedbacks_json = response.json()
    step_print("Got raw feedbacks.")
    return feedbacks_json

def get_feedbacks_by_root(root: int) -> list[dict]:
    step_print(f"Getting nice feedbacks by root...")
    for i in range(1, 5):
        if get_raw_feedbacks_by_root_index(root, i)['feedbacks']:
            feedbacks_json = get_raw_feedbacks_by_root_index(root, i)
            # save_log_file("parsers/wb/debug/tmp.json", feedbacks_json)
            break
        continue
    try:
        feedbacks_info = []
        for feedback in feedbacks_json['feedbacks']:
            feedbacks_info.append({ 
                "plus": feedback['pros'],
                "minus": feedback['cons'],
                "comment": feedback['text'],
                "rating": feedback['productValuation']
            })
        step_print("Got nice feedbacks.")
        return feedbacks_info
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Json access error") from exc

def get_all_feedbacks(product_id: int) -> list[dict]:
    step_print(f"Getting all feedbacks for id: {product_id}...")
    """
        Получает все отзывы на товар по его id. <br>

        Возвращает список словарей формата: <br>
        ```json
        [
            {
                "comment": ___,
                "pros": ___,
                'cons': ___,
                'rating': ___
            },
            ...
        ]
    """
    root = get_root_by_id(product_id)
    feedbacks = get_feedbacks_by_root(root)
    step_print(f"Got all feedbacks for one product {product_id}.")
    return feedbacks

# print(get_all_feedbacks(205062857))