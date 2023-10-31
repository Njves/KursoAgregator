"""Модуль парсинга с https://gb.ru/"""
import csv
import re
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
import requests


def get_name(soup):
    """
    Функция извлекает имя курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Имя курса, извлеченное из объекта BeautifulSoup.
    """
    name = soup.find('title').get_text(strip=True)
    pattern = '«(.*?)»'
    result = re.search(pattern, name)
    if result:
        return result.group(1)
    return name


def get_description(soup):
    """
    Функция извлекает описание курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Описание курса, извлеченное из объекта BeautifulSoup.
    """
    description = soup.find("meta", attrs={'name': 'description'})
    return description["content"]


def get_price(soup):
    """
    Функция извлекает цену курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Цена курса, извлеченная из объекта BeautifulSoup.
    """
    element = soup.find('span', attrs={'data-price': 'price_main'})
    price = ""
    if element:
        price = element.text.strip().removeprefix("от ")
        price = price + ' ₽' if not price.endswith(" ₽") else price
    if not price or price == ' ₽':
        price_tag = soup.find('div', class_='gkb-package-card__header-new')
        if price_tag:
            price = price_tag.get_text().strip().removeprefix("от ")
    return price


def get_authors(soup: webdriver.Chrome):
    """
    Функция извлекает авторов курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Авторы курса, извлеченная из объекта BeautifulSoup.
    """
    teacher_cards = soup.find_all(class_="teacher-card-new__title")
    authors = [card.get_text(strip=True) for card in teacher_cards]
    return authors


def get_duration(soup):
    """
    Функция извлекает продолжительность курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Продолжительность курса, извлеченная из объекта BeautifulSoup.
    """
    meta_tag = soup.find('meta', property='og:description')
    duration = ''
    if meta_tag:
        content = meta_tag['content']
        duration_index = content.find('Длительность обучения:')
        if duration_index != -1:
            duration = content[duration_index:].split(':')[1].split('.')[0]
    if not duration:
        p_tag = soup.find('p', class_='gkb-promo__text-secondary')
        if p_tag:
            text = p_tag.get_text()
            split_text = text.split()
            for i in range(len(split_text) - 1):
                if split_text[i] == 'месяцев':
                    duration = split_text[i - 1] + " " + split_text[i]
    return duration.strip()


def get_technology(soup):
    """
    Функция извлекает технологии курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Технологии курса, извлеченная из объекта BeautifulSoup.
    """
    tags = ['SQL', 'Python', 'JavaScript', 'Kotlin', 'Linux',
            'Golang', 'Java', 'Аналитика данных', 'Machine Learning',
            'Веб-разработка', 'Тестирование', 'C#', '1C']
    matching_tags = []
    img_tags = soup.find_all('img')
    for tag in img_tags:
        alt_text = tag.get('alt')
        if alt_text in tags:
            matching_tags.append(alt_text)
    return matching_tags


def process_course(course):
    """
    Функция обрабатывает курс, извлекая информацию о нем с веб-страницы.
    :param course: URL курса, который нужно обработать.
    :return: Кортеж с информацией о курсе в следующем формате:
        (URL, Name, Authors, Description, Duration, Price, [])
        Если информация не найдена, возвращает None.
    """
    hdr = {'User-Agent': 'Chrome/118.0.0.0'}
    request = requests.get(course, headers=hdr)
    soup = BeautifulSoup(request.text, 'html.parser')
    name = get_name(soup)
    description = get_description(soup)
    price = get_price(soup)
    authors = get_authors(soup)
    duration = get_duration(soup)
    technology = get_technology(soup)
    if not technology:
        return
    return (request.url, name, authors,
            description, duration, price, technology)


def geekbrains_parser_courses_parallel():
    """
    Парсит с сайта https://gb.ru/ ссылку на курс, имя, описание автора, цену,
    длительность и технологии курса, после чего сохраняет в csv файл.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)
    urls = ['https://gb.ru/courses/testing', 'https://gb.ru/courses/ml',
            'https://gb.ru/courses/programming', 'https://gb.ru/courses/it']
    course_links = []
    for url in urls:
        driver.get(url)
        elements = driver.find_elements(
            "css selector", 'a.card_full_link')
        course_links.extend([elem.get_attribute('href') for elem in elements])
    courses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for course in set(course_links):
            if course not in [course[0] for course in courses]:
                futures.append(executor.submit(process_course, course))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                if result not in courses:
                    if result not in [course[0] for course in courses]:
                        courses.append(result)
    csv_columns = ['URL', 'Name', "Authors",
                   "Description", 'Duration', 'Price', 'Technology']
    driver.quit()
    with open("app/parsers/geekbrains.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for course in courses:
            writer.writerow(course)


if __name__ == "__main__":
    geekbrains_parser_courses_parallel()
