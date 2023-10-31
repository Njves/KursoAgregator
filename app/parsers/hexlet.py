"""Модуль парсинга со Hexlet"""
import csv
import re
from bs4 import BeautifulSoup
import requests
import concurrent.futures


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


def get_duration(soup):
    """
    Функция извлекает продолжительность курса из объекта BeautifulSoup.
    :param soup: Объект BeautifulSoup, представляющий HTML-контент страницы.
    :return: Продолжительность курса, извлеченная из объекта BeautifulSoup.
    """
    duration_tag = soup.find('div', class_='mb-2 text-body-secondary')
    duration = duration_tag.get_text().strip()
    return duration.removeprefix("Продолжительность ")


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
    price = '3900 ₽'
    authors = ['Hexlet']
    duration = get_duration(soup)
    return (request.url, name, authors,
            description, duration, price, [])


def hexlet_parser_courses_parallel() -> None:
    """
    Парсит с сайта hexlet ссылку на курс, имя, описание автора, цену,
    длительность и технологии курса, после чего сохраняет в csv файл.
    """
    courses = []
    hdr = {'User-Agent': 'Chrome/119.0.0.0'}
    catalogs = {'https://ru.hexlet.io/courses-python': 'Python',
                'https://ru.hexlet.io/courses-sql': 'SQL',
                'https://ru.hexlet.io/courses-java': 'Java'}
    for catalog, technology in catalogs.items():
        request = requests.get(catalog, headers=hdr)
        soup = BeautifulSoup(request.text, 'html.parser')
        links = soup.find_all('a', class_='stretched-link')
        course_links = []
        for link in links:
            if link['href'].startswith("/courses"):
                course_links.append(link['href'])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for course in course_links:
                url_cour = 'https://ru.hexlet.io/' + course
                if url_cour not in [course[0] for course in courses]:
                    futures.append(executor.submit(process_course, url_cour))
                else:
                    index = [course[0] for course in courses].index(url_cour)
                    courses[index][-1].append(technology)
            for future in concurrent.futures.as_completed(futures):
                if future.result() is not None:
                    courses.append(future.result())
                    courses[-1][-1].append(technology)
    csv_columns = ['URL', 'Name', "Authors",
                   "Description", 'Duration', 'Price', 'Technology']
    with open("app/parsers/hexlet.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for course in courses:
            writer.writerow(course)


if __name__ == "__main__":
    hexlet_parser_courses_parallel()
