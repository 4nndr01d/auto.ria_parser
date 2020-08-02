import csv


class FileSaver:
    def __init__(self, file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в UAH', 'Город'])

    @staticmethod
    def save(item, path):
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])
