from time import sleep

import requests
import threading
import datetime


def night_update():
    is_updated = False
    while True:
        print('Нужно обновить' if not is_updated else 'Ждем обновления')
        if datetime.datetime.now().hour == 16 and not is_updated:
            is_updated = True
            requests.post('http://127.0.0.1:5000/parse')
        if datetime.datetime.now().hour == 17 and is_updated:
            is_updated = False
        sleep(1)
threading.Thread(target=night_update).start()
