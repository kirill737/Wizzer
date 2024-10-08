"""
DOCSTRING TEMPLATE
"""
import requests

def get_root_by_id(product_id: int) -> int:
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
    response = requests.get(
        f"https://feedbacks{index}.wb.ru/feedbacks/v2/{root}",
        timeout=10
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Wrong response code: {response.status_code}"
        )
    feedbacks_json = response.json()
    return feedbacks_json

def get_feedbacks_by_root(root: int) -> list[dict]:
    for i in range(1, 5):
        if get_raw_feedbacks_by_root_index(root, i)['feedbacks']:
            feedbacks_json = get_raw_feedbacks_by_root_index(root, i)
            break
        continue
    try:
        feedbacks_info = []
        for feedback in feedbacks_json['feedbacks']:
            feedbacks_info.append({
                "text": feedback['text'], 
                "pros": feedback['pros'],
                "cons": feedback['cons']
            })
        return feedbacks_info
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Json access error") from exc

def get_all_feedbacks(product_id: int) -> dict:
    root = get_root_by_id(product_id)
    feedbacks = get_feedbacks_by_root(root)
    return feedbacks


# print(get_all_feedbacks(177900370))
