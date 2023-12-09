from time import sleep

import requests
import threading
import datetime
import logging
from logging.handlers import RotatingFileHandler


def night_update():
    """
    Клиент прокидывает запрос серверу на парсинг
    курсов, в 12 ночи, после исполнения меняет
    :return:
    """
    is_updated = False
    while True:
        if datetime.datetime.now().hour == 0 and not is_updated:
            print('Отправил запрос')
            is_updated = True
            requests.post('http://127.0.0.1:5000/parse')
        if datetime.datetime.now().hour == 1 and is_updated:
            is_updated = False
        sleep(1)


threading.Thread(target=night_update).start()
