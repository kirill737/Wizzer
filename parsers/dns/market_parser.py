from random import randint
from time import sleep as pause
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import re

DNS_URL = "https://www.dns-shop.ru"


def scroll_to_bottom(driver):
    """Прокручивает страницу до самого низа."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Прокрутка до самого низа страницы
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Ждем некоторое время для загрузки контента
        pause(randint(3, 5))

        # Снова получаем текущую высоту страницы после прокрутки
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Если высота не изменилась, значит мы достигли конца страницы
        if new_height == last_height:
            break

        last_height = new_height

def load_all_reviews(driver, url):
    """Загружает все отзывы, нажимая кнопку 'Показать ещё'."""
    driver.get(url)
    pause(randint(10, 13))  # Задержка для полной загрузки страницы
    scroll_to_bottom(driver)
    count = 1
    while True:
        try:
            # Ищем кнопку "Показать ещё" и нажимаем на неё
            show_more_button = driver.find_element(
                "xpath", "//button[text()='Показать ещё']")
            show_more_button.click()
            print(f"Нажал на кнопку {count} раз")
            count += 1
            pause(randint(2, 5))  # Ждем после нажатия
        except NoSuchElementException:
            # Если кнопка не найдена, значит все отзывы загружены
            print("Все отзывы загружены.")
            break

    # Возвращаем полный HTML-код после загрузки всех отзывов
    return driver.page_source

def parse_feedbacks_page(driver, url: str):
    print(url)
    code = load_all_reviews(driver, url)
    pause(randint(4, 8))
    soup = BeautifulSoup(code, 'lxml')
    with open('feedbacks_page.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    feedbacks = {}
    return 1

def parse_characteristics_page(driver, url: str):
    """ Парсит страницу товара по ссылке."""
    driver.get(url)
    pause(randint(7, 11))
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # page_source = driver.page_source

    # Сохраняем HTML-код в файл
    with open('test.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    products = soup.find_all('div', class_="catalog-product ui-button-widget")
    with open('div.html', 'w', encoding='utf-8') as file:
        file.write(products[0].prettify())
    print("Point 1")
    print(products)
    for product in products:
        print("Point 2")
        name = product.find(
            'a', class_="catalog-product__name ui-link ui-link_black").find('span').text
        rate = product.find('a', class_="catalog-product__rating").get("data-rating")
        price = product.find('span', class_="product-buy__prev").text
        feedbacks_link = product.find('a', class_="catalog-product__rating").get('href')
        print(f"name: {name}")
        print(f"rate: {rate}")
        print(f"price: {price}")
        print(f"feedbacks_link: {feedbacks_link}")
        feedbacks = parse_feedbacks_page(driver, DNS_URL + feedbacks_link)
        break
    # fullnames = soup.find_all('a', class_="catalog-product__name ui-link ui-link_black")





try:
    driver = uc.Chrome()

    parse_characteristics_page(
        driver, "https://www.dns-shop.ru/catalog/17a8a01d16404e77/?f[al]=4pv&p=2")
finally:
    driver.quit()
