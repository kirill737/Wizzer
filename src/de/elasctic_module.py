import json

from elasticsearch import Elasticsearch, helpers


class ElasticSearchHelper:
    def __init__(self, host, username, password):
        self.es = Elasticsearch(
            hosts=[host],
            basic_auth=(username, password)
        )

    # 1. Проверка соединения с сервером
    def check_connection(self):
        try:
            if self.es.ping():
                print("Соединение с сервером установлено!")
            else:
                print("Ошибка: невозможно подключиться к серверу.")
        except Exception as e:
            print(f"Ошибка при подключении к серверу: {e}")

    # 2. Отображение всех документов из индекса по запросу
    def search_documents(self, index_name,  field, query_string):
        try:
            query = {
                "query": {
                    "match": {
                        field: query_string  # Поиск по всем полям
                    }
                }
            }
            response = self.es.search(index=index_name, body=query)
            hits = response["hits"]["hits"]
            
            if hits:
                print(f"Найдено {len(hits)} документов, соответствующих запросу '{query_string}':")
                for i, hit in enumerate(hits, start=1):
                    print(f"\nДокумент {i}:")
                    print(json.dumps(hit["_source"], indent=4, ensure_ascii=False))
            else:
                print(f"Нет документов, соответствующих запросу '{query_string}'.")
        except Exception as e:
            print(f"Ошибка при поиске документов в индексе '{index_name}': {e}")

    # 3. Добавление документов из файла в индекс
    def add_documents(self, index_name, file_path: str = None, data: list = None):
        try:
            if data is None:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
            
            actions = [
                {
                    "_index": index_name,
                    "_source": doc
                }
                for doc in data
            ]
            
            helpers.bulk(self.es, actions)
            print(f"Успешно добавлено {len(actions)} документов в индекс '{index_name}'.")
        except Exception as e:
            print(f"Ошибка при добавлении документов в индекс '{index_name}': {e}")

    # 4. Удаление документов из индекса по тексту или очистка индекса
    def delete_documents(self, index_name, field, query_string=""):
        try:
            if query_string:
                body = {"query": {"match": {field: query_string}}}
            else:
                body = {"query": {"match_all": {}}}
            response = self.es.delete_by_query(index=index_name, body=body)
            deleted = response.get("deleted", 0)
            print(f"Удалено {deleted} документов из индекса '{index_name}'.")
        except Exception as e:
            print(f"Ошибка при удалении документов из индекса '{index_name}': {e}")

    # 5. Удаление индекса
    def delete_index(self, index_name):
        try:
            self.es.indices.delete(index=index_name, ignore=[400, 404])
            print(f"Индекс '{index_name}' успешно удалён.")
        except Exception as e:
            print(f"Ошибка при удалении индекса '{index_name}': {e}")

    # 6. Создание индекса
    def create_index(self, index_name, settings=None):
        try:
            if settings is None:
                settings = {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    }
                }
            self.es.indices.create(index=index_name, body=settings, ignore=400)
            print(f"Индекс '{index_name}' успешно создан.")
        except Exception as e:
            print(f"Ошибка при создании индекса '{index_name}': {e}")
