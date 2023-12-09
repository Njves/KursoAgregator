import datetime
import threading
from time import sleep

import requests


def send_request():
    return requests.post('http://127.0.0.1:5000/parse')

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
            send_request()
        if datetime.datetime.now().hour == 1 and is_updated:
            is_updated = False
        sleep(1)


def execute():
    threading.Thread(target=night_update).start()


if __name__ == '__main__':
    send_request()
