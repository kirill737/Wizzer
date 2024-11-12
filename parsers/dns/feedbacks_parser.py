from helper import *
import requests
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
            'rating': ___
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
            'rating': opinion['rating']
            # "name": opinion['user']['name']
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
        # TO DO:  Останавливать парсинг при пустых отзывах
        if not part_of_feedbacks:
            break
        all_feedbacks += part_of_feedbacks
        if offset % 100 == 0:
            debug_print(f"offset: {offset} parts: {len(part_of_feedbacks)}, all: {len(all_feedbacks)}")
        offset += 10
    step_print("End getting all feedbacks")
    return all_feedbacks