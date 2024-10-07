from bs4 import BeautifulSoup
import requests
import json

# Чтобы сработало надо создать файл со своими куками в json
with open('cookies.json', 'r', encoding='utf-8') as file:
    cookies = json.load(file)

# Заголовки для имитации браузера
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
}

# URL страницы
url = 'https://www.wildberries.ru/catalog/179755083/feedbacks?imtId=175097505'

# Отправляем GET-запрос с куками и заголовками
response = requests.get(url, headers=headers, cookies=cookies)

# Проверяем результат
if response.status_code == 200:
    # Сохраняем результат в файл или анализируем с помощью BeautifulSoup
    with open('wildberries_feedbacks.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
else:
    print(f"Ошибка: {response.status_code}")




def parse_feedback_text(url):
    # response = requests.get(url)
    with open(url, 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Если запрос успешен
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        with open('ttt.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        # Ищем все элементы с классом 'feedback__text--item'
        feedback_items = soup.find_all('span', class_='feedback__text--item')
        print(feedback_items)
        # Извлекаем текст из каждого найденного элемента и собираем в список
        feedback_texts = [item.get_text(strip=True) for item in feedback_items]

        return feedback_texts
    else:
        return f"Ошибка {response.status_code} при запросе страницы"

url = 'https://www.wildberries.ru/catalog/179740419/feedbacks?imtId=173747980&size=297218388'

url = 'wildberries_feedbacks.html'
feedback_texts = parse_feedback_text(url)

for feedback in feedback_texts:
    print(feedback)

