import re
import json

import pandas as pd


# Функция для удаления смайликов
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002500-\U00002BEF"  # Chinese characters
        "\U00002702-\U000027B0"
        "\U00002700-\U000027BF"
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001F018-\U0001F270"
        "\U0001F200-\U0001F2FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002600-\U000026FF"
        "\U00002300-\U000023FF"
        "\U00002B50-\U00002B55"
        "\U0001F680-\U0001F6FF"
        "\u200d"  # Zero-width joiner
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\u3030"
        "\ufe0f"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r' ', text)


# Функция стандартизации текста
def standardize_text(text):
    text = text.lower()  # Приведение к нижнему регистру
    text = re.sub(r'[^\w\s.,!?]', ' ', text)  # Удаление лишних символов
    text = re.sub(r'\s+', ' ', text)  # Удаление лишних пробелов
    text = text.strip()  # Удаление пробелов в начале и конце строки
    return text


def gen(path_to_json: str):
    with open(path_to_json, "r", encoding="utf-8") as f:
        docs = json.load(f)

    total = len(docs)
    ids = set()
    for doc in docs:
        ids.add(doc.get("id"))
        feedbacks = doc.get("feedbacks", [])
        if (not isinstance(feedbacks, int)) and (len(feedbacks)):
            for feedback in feedbacks:
                yield feedback
    print("total", total)
    print("ids", len(ids))


def make_exceles(data):
    cols = [
        "Скорость", "Камера", "Цена", "Экран", "Звук", "Емкость", 
        "Подлинность", "Эстетичность", "Функциональность", "Комплектация",
    ]
    for field in data:
        comments = data.get(field)
        df = pd.DataFrame({field: comments})
        for col in cols:
            df[col] = None
        df.to_excel(f"Разметка_{field}.xlsx", index=False)


if __name__ == "__main__":
    PATH_TO_JSON = "src/parsed_feedbacks/dns_example.json"

    data = {"plus": [], "minus": [], "comment": []}
    standart_values = set()

    for feedback in gen(PATH_TO_JSON):
        for field in ["plus", "minus", "comment"]:
            text = feedback.get(field, "")
            
            if len(text) < 5 or text.count(" ") == 0:
                continue
            
            text = remove_emojis(text)

            standart_val = standardize_text(text)

            if standart_val not in standart_values and len(standart_val) > 4:
                standart_values.add(standart_val)
                data[field].append(text)

    print("uniq values:", len(standart_values))

    with open("prepared.json", "w", encoding="utf-8") as f:  # Промежуточное сохранение данных
        json.dump(data, f, ensure_ascii=False, indent=4)


    make_exceles(data)  # Таблицы для удобной разметки для обучения модели