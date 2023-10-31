"""Модуль парсинга со степика"""
import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver, common
import requests
import concurrent.futures


def get_price(driver: webdriver.Chrome):
    """
    Функция находит цену на странице сайта.
    :param driver: Объект веб-драйвера Chrome.
    :return: Цена курса, если она есть на странице, иначе возвращает None.
    Если цена равна "Поступить на курс", функция возвращает "0".
    Если цена начинается с "Купить за", функция возвращает сумму.
    """
    price = driver.find_element(
        "css selector", 'div.course-join-button button.button_with-loader')
    try:
        price = price.text.strip()
    except Exception:
        return None
    if price == "Поступить на курс":
        return "0"
    if price.startswith("Купить за"):
        return price.split('Купить за ')[-1]
    return None


def get_authors(driver: webdriver.Chrome):
    """
    Функция извлекает информацию об авторах курса с веб-страницы.
    :param driver: Объект веб-драйвера Chrome.
    :return: Список авторов, если есть на странице, иначе возвращает None.
    Если авторы не найдены, функция возвращает "Null".
    """
    try:
        authors = driver.find_elements(
            "css selector", 'div.author-widget__content a')
        authors = [author.text.strip() for author in authors]
    except common.exceptions.NoSuchElementException:
        authors = []
    if authors:
        return authors
    try:
        authors = driver.find_elements(
            "css selector", 'div.course-index__aside-authors span.user-avatar__name')
        authors = [author.text.strip() for author in authors]
        return authors
    except common.exceptions.NoSuchElementException:
        pass
    return "Null"


def get_duration(driver: webdriver.Chrome):
    """
    Функция находит информацию о продолжительности курса на странице.
    :param driver: Объект веб-драйвера Chrome.
    :return: Продолжительность курса, если она есть на странице,
    иначе возвращает None.
    """
    try:
        duration = driver.find_element(
            "xpath", "//div[contains(@class, 'course-index__def-row')" +
            "and contains(dt, 'Время прохождения курса')]/dd").text.strip()
    except common.exceptions.NoSuchElementException:
        duration = None
    return duration


def process_course(course):
    """
    Функция обрабатывает курс, извлекая информацию о нем с веб-страницы.
    :param course: URL курса, который нужно обработать.
    :return: Кортеж с информацией о курсе в следующем формате:
        (URL, Name, Authors, Description, Duration, Price, [])
        Если информация не найдена, возвращает None.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    hdr = {'User-Agent': 'Chrome/118.0.0.0'}
    request = requests.get(course, headers=hdr)
    soup = BeautifulSoup(request.text, 'html.parser')
    name = soup.find("meta", property="og:title")
    description = soup.find("meta", attrs={'name': 'description'})
    driver.get(course)
    price = get_price(driver)
    authors = get_authors(driver)
    duration = get_duration(driver)
    if price is None or duration is None or not description or not authors:
        return None
    return (course, name["content"], authors,
            description["content"], duration, price, [])


def stepik_parser_courses_parallel() -> None:
    """
    Парсит со степика ссылку на курс, имя, описание автора, цену,
    длительность и технологии курса, после чего сохраняет в csv файл.
    """
    catalogs = {42: "SQL", 153: "Python", 237: "JavaScript", 54: "Kotlin",
                57: "Linux", 156: "Golang", 62: "Java", 236:
                "Аналитика данных", 226: "Machine Learning",
                181: "Веб-разработка", 219: "Тестирование",
                210: "C#"}
    courses = []
    for catalog, technology in catalogs.items():
        url = 'https://stepik.org/catalog/' + str(catalog)
        hdr = {'User-Agent': 'Chrome/118.0.0.0'}
        request = requests.get(url, headers=hdr)
        soup = BeautifulSoup(request.text, 'lxml')
        pattern = re.compile(r'\/course\/\d+')
        course_links = [link['href'] for link in soup.find_all(
            'a', href=True) if pattern.match(link['href'])]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for course in set(course_links):
                url_cour = 'https://stepik.org' + course + "/info"
                if url_cour not in [course[0] for course in courses]:
                    futures.append(executor.submit(
                        process_course, url_cour))
                else:
                    index = [course[0] for course in courses].index(url_cour)
                    courses[index][-1].append(technology)
            for future in concurrent.futures.as_completed(futures):
                if future.result() is not None:
                    courses.append(future.result())
                    courses[-1][-1].append(technology)

    csv_columns = ['URL', 'Name', "Authors",
                   "Description", 'Duration', 'Price', 'Technology']
    try:
        with open("app/parsers/stepik.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for course in courses:
                writer.writerow(course)
    except IOError:
        print("Ошибка при записи в файл CSV")


if __name__ == "__main__":
    stepik_parser_courses_parallel()
