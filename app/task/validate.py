import csv
import pathlib
from config import basedir



def validate_data():
    print("Начали валидацию данных")
    csv_files = pathlib.Path(basedir, 'app', 'parsers').glob('*.csv')
    for file_name in csv_files:
        path = pathlib.Path(file_name)
        with open(path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            data = []
            for row in csv_reader:
                if any(not val for val in row.values()):
                    print(row)
                    continue
                if row['Duration']:
                    duration: int = int(''.join([i for i in row['Duration'] if i.isnumeric()]))
                    if 'дн' in row['Duration']:
                        duration *= 24
                    if 'неде' in row['Duration']:
                        duration *= 168
                    if 'мес' in row['Duration']:
                        duration *= 168 * 30
                    row['Duration'] = duration
                if row['Price']:
                    row['Price']: int = int(''.join([i for i in row['Price'] if i.isnumeric()]))
                data.append(row)
        with open(path, 'w', encoding='utf-8') as file:
            fields = csv_reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
        print("Закончили валидацию данных")