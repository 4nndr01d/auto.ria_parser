import requests
from bs4 import BeautifulSoup

from file_saver import FileSaver

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://auto.ria.com'


class CarParser:
    def get_html(self, url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    def get_pages_count(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find_all('span', class_='page-item mhide')
        if pagination:
            return int(pagination[-1].get_text())
        else:
            return 1

    def get_mark(self, soup):
        mark = soup.find('div', class_='fast_buttons_name')
        return mark.find('strong', class_='mhide').get_text(strip=True)+'.csv'

    def get_content(self, soup):
        items = soup.find_all('div', class_='proposition')
        for item in items:
            header = item.find('h3', class_='proposition_name')
            title = header.find('strong').get_text(strip=True)
            link = header.find('a').get('href')
            prices = item.find('div', class_='proposition_price')
            usd = prices.find('span', class_='green').get_text(strip=True)
            uah = prices.find('span', class_='grey size13')
            if uah:
                uah = uah.get_text(strip=True)
            else:
                uah = 'None'
            city = item.find('div', class_='proposition_region')
            city = city.find('strong').get_text(strip=True)

            yield {
                'title': title,
                'link': HOST + link,
                'usd_price': usd,
                'uah_price': uah,
                'city': city
            }


def parse():
    car_parser = CarParser()
    url = input('Введите URL с сайта auto.ria.com из раздела новые автомобили:')
    url = url.strip()
    html = car_parser.get_html(url)
    if html.status_code != 200:
        print('Error')
        return

    pages_count = car_parser.get_pages_count(html.text)
    soup = BeautifulSoup(html.text, 'html.parser')
    mark = car_parser.get_mark(soup)
    saver = FileSaver(mark)
    for page in range(1, pages_count + 1):
        print(f'Парсинг страницы {page} из {pages_count}...')
        html = car_parser.get_html(url,params = {'page': page})
        soup = BeautifulSoup(html.text, 'html.parser')
        for new_car in car_parser.get_content(soup):
            saver.save(new_car, mark)

    print(f'Файл записан')


parse()
