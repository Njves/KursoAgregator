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
    try:
        price = driver.find_element(
            "css selector", 'div.course-join-button button.button_with-loader')
        price = price.text.strip()
    except Exception:
        return None
    if price == "Поступить на курс":
        return "0"
    if price.startswith("Купить за"):
        return price.split('Купить за ')[-1]
    return None


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
        (URL, Name, Description, Duration, Price, [])
        Если информация не найдена, возвращает None.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    hdr = {'User-Agent': 'Chrome/118.0.0.0'}
    request = requests.get(course, headers=hdr)
    if request.status_code != 200:
        return None
    soup = BeautifulSoup(request.text, 'html.parser')
    name = soup.find("meta", property="og:title")
    tags = ['SQL', 'Python', 'JavaScript', 'Kotlin', 'Linux',
            'Golang', 'Java', 'Аналитика данных', "Machine Learning",
            'Веб-разработка', 'Тестирование', 'C#', '1C', "Swift", "PHP",
            "Dart", "Android",  "IOS"]
    description = soup.find("meta", attrs={'name': 'description'})
    driver.get(course)
    price = get_price(driver)
    duration = get_duration(driver)
    if price is None or duration is None or not description:
        return None
    if not name["content"] or not description["content"]:
        return None
    course_tags = []
    for tag in tags:
        if tag in description["content"] or tag in name["content"] :
            course_tags.append(tag) 
    return (course, name["content"],
            description["content"], duration, price, course_tags)


def stepik_parser_courses_parallel() -> None:
    """
    Парсит со степика ссылку на курс, имя, описание автора, цену,
    длительность и технологии курса, после чего сохраняет в csv файл.
    """
    print('Начался парсинг https://stepik.org')
    catalogs = {42: "SQL", 153: "Python", 237: "JavaScript", 54: "Kotlin",
                57: "Linux", 156: "Golang", 62: "Java", 236:
                "Аналитика данных", 226: "Machine Learning",
                181: "Веб-разработка", 219: "Тестирование",
                210: "C#", 315: "Swift", 316: "PHP", 321: "Dart", 324: "1C"}
    courses = []
    for catalog, technology in catalogs.items():
        url = 'https://stepik.org/api/course-lists/' + str(catalog)
        hdr = {'User-Agent': 'Chrome/118.0.0.0'}
        request = requests.get(url, headers=hdr)
        course_ids = request.json()["course-lists"][0]["courses"]
        with concurrent.futures.ThreadPoolExecutor(10) as executor:
            futures = []
            for course_id in set(course_ids):
                url_cour = 'https://stepik.org/course/' + str(course_id) + "/info"
                if url_cour not in [course[0] for course in courses]:
                    futures.append(executor.submit(
                        process_course, url_cour))
                else:
                    index = [course[0] for course in courses].index(url_cour)
                    if technology not in courses[index][-1]:
                        courses[index][-1].append(technology)
            for future in concurrent.futures.as_completed(futures):
                if future.result() is not None:
                    courses.append(future.result())
                    if technology not in courses[-1][-1]:
                        courses[-1][-1].append(technology)

    csv_columns = ['URL', 'Name',
                   "Description", 'Duration', 'Price', 'Technology']
    try:
        with open("app/parsers/stepik.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for course in courses:
                if course[-1] != ["Аналитика данных"]:
                    writer.writerow(course)
    except IOError:
        print("Ошибка при записи в файл CSV")
    print('Закончился парсинг https://stepik.org')


if __name__ == "__main__":
    import time
    s = time.time()
    stepik_parser_courses_parallel()
    print(time.time() - s)
