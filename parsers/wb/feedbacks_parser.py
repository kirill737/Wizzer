"""
DOCSTRING TEMPLATE
"""
import json
import re
from pathlib import Path
import requests
from models import InputJSON, OutputProduct

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
    print(type(root_json))
    try:
        root_value = root_json['data']['products'][0]['root']
        return root_value
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Json access error") from exc

def get_raw_feedbacks_by_root(root: int) -> list[str]:
    response = requests.get(
        f"https://feedbacks1.wb.ru/feedbacks/v2/{root}",
        timeout=10
    )
    feedbacks_list = []
    if response.status_code != 200:
        raise RuntimeError(
            f"Wrong response code: {response.status_code}"
        )
    feedbacks_json = response.json()
    try:
        # feedbacks_count = feedbacks_json['feedbackCount']
        for feedback in feedbacks_json['feedbacks']:
            feedbacks_list.append(feedback['text'])
            
        return feedbacks_list
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Json access error") from exc
root = get_root_by_id(179755083)
print(root)
feedbacks = get_raw_feedbacks_by_root(root)
print(feedbacks)
