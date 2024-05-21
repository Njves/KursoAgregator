import requests
from faker import Faker
import random
def generate_review():
    fake = Faker()
    base_url = 'http://127.0.0.1:5000/review/'

    # Список курсов, куда будут отправляться отзывы
    course_ids = [1]
    # Число отзывов на 1 курс
    n = 10
    user_id = 1
    for course_id in course_ids:
        url = f'{base_url}{course_id}'
        for _ in range(n):
            text = fake.text()
            rating = random.randint(1, 5)
            data = {
                'text': text,
                'rating': rating,
                'user_id': user_id
            }
            response = requests.post(url, data=data)

if __name__ == '__main__':
    generate_review()