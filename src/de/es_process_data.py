import os
import sys
sys.path.append(os.getcwd())
import json

from src.de.elasctic_module import ElasticSearchHelper
from src.ml.inference import (
    process_reviews, 
    load_model,
    postprocess_logits,
)
from src.config import (
    ES_HOST,
    ES_USERNAME,
    ES_PASSWORD,
    ES_INDEX_NAME,
    DATA_PATH,
    marks_mapping,
)


def reviews_generator(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for obj in data:
        yield obj


es_helper = ElasticSearchHelper(ES_HOST, ES_USERNAME, ES_PASSWORD)

# 1. Проверка соединения
print("=== Проверка соединения с сервером ===")
es_helper.check_connection()

# 2. Создание индекса
print("\n=== Создание индекса ===")
es_helper.create_index(ES_INDEX_NAME)

# 3. Загрузка документов из файла
print("\n=== Обработка документов ===")

model, tokenizer = load_model()

batch = []
for obj in reviews_generator(DATA_PATH):
    obj["neutral_sides"] = []
    obj["advantages"] = []
    obj["disadvantages"] = [] 

    reviews = obj.pop("feedbacks")
    reviews = reviews if isinstance(reviews, list) else []
    if len(reviews):
        marks = process_reviews(model, tokenizer, reviews)
        for mark, review in zip(marks, reviews):
            review["marks"] = mark.tolist()
        
        mean_mark = marks.mean(axis=0)
        obj["mean_mark"] = mean_mark.tolist()
        
        for i, label in enumerate(postprocess_logits(mean_mark)):
            if label == -1:
                obj["disadvantages"].append(i)
            elif label == 0:
                obj["neutral_sides"].append(i)
            else:
                obj["advantages"].append(i)
    else:
        obj["mean_mark"] = [0] * len(marks_mapping)
        obj["neutral_sides"] = list(range(len(marks_mapping)))

    obj["feedbacks"] = reviews

    obj["link"] = "https://yandex.ru/video/preview/3772920970274748489"  # Linkin Park "Crawling"

    batch.append(obj)

    if len(batch) == 64:
        with open("done_batches.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(batch, ensure_ascii=False) + "\n")
           
        print("loading batch")
        
        try:
            es_helper.add_documents(ES_INDEX_NAME, data=batch)
            batch = []
        except Exception as e:
            print(e)
            raise

        print("success")

if len(batch):
    with open("done_batches.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(batch, ensure_ascii=False) + "\n")
    try:
        es_helper.add_documents(ES_INDEX_NAME, data=batch)
        del batch
    except Exception as e:
        print(e)
        raise

# # 4. Поиск документов по запросу
# print("\n=== Поиск документов ===")
# es_helper.search_documents(ES_INDEX_NAME, "brand", "Apple")

# # 5. Удаление документов по запросу
# print("\n=== Удаление документов по запросу ===")
# es_helper.delete_documents(ES_INDEX_NAME, "brand", "Apple")

# # 6. Поиск документов по запросу
# print("\n=== Поиск документов ===")
# es_helper.search_documents(ES_INDEX_NAME, "brand", "Apple")

# 7. Удаление индекса
# print("\n=== Удаление индекса ===")
# es_helper.delete_index(ES_INDEX_NAME)