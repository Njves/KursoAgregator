"""Модуль парсинга со топ академии"""
import csv
from bs4 import BeautifulSoup
import requests
import concurrent.futures


def get_name(soup):
    """
    Функция извлекает имя курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Имя курса, извлеченное из объекта BeautifulSoup.
    """
    name = soup.find('h1', class_='banner-top__title').get_text().strip()
    return name.removeprefix("Курс: ")


def get_description(soup):
    """
    Функция извлекает описание курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Описание курса, извлеченное из объекта BeautifulSoup.
    """
    description = soup.find("p", class_='banner-top__text')
    return description.get_text().strip()


def get_price(soup):
    """
    Функция извлекает цену курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Цена курса, извлеченная из объекта BeautifulSoup.
    """
    price_tag = soup.find('p', class_='education-form__cost')
    price = price_tag.get_text().strip().removesuffix("/курс")
    return price


def get_duration(soup):
    """
    Функция извлекает продолжительность курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Продолжительность курса, извлеченная из объекта BeautifulSoup.
    """
    duration_tag = soup.find('p', class_='education-form__schedule--duration')
    duration = duration_tag.get_text().strip()
    duration = " ".join(duration.split()[0:2])
    return duration


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
    authors = ['Компьютерная Академия TOP']
    duration = get_duration(soup)
    technology = None
    return (request.url, name, authors,
            description, duration, price, technology)


def top_academy_parser_courses_parallel() -> None:
    """
    Парсит с сайта топ академии ссылку на курс, имя, описание автора, цену,
    длительность и технологии курса, после чего сохраняет в csv файл.
    """
    courses = []
    hdr = {'User-Agent': 'Chrome/119.0.0.0'}
    url = 'https://online.top-academy.ru/it_courses_for_adults'
    request = requests.get(url, headers=hdr)
    soup = BeautifulSoup(request.text, 'html.parser')
    course_links = soup.find_all('a', class_='course__item')
    course_links = [link['href'] for link in course_links]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for course in course_links:
            url_cour = 'https://online.top-academy.ru' + course
            if url_cour not in [course[0] for course in courses]:
                futures.append(executor.submit(process_course, url_cour))
        for future in concurrent.futures.as_completed(futures):
            if future.result() is not None:
                courses.append(future.result())
    csv_columns = ['URL', 'Name', "Authors",
                   "Description", 'Duration', 'Price', 'Technology']
    with open("app/parsers/top-academy.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for course in courses:
            writer.writerow(course)


if __name__ == "__main__":
    top_academy_parser_courses_parallel()
