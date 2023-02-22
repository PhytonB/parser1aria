import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

class AutoParser:
    CSV = 'auto.csv'
    HOST = 'https://auto.ria.com/'
    URL = 'https://auto.ria.com/uk/legkovie/'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    def __init__(self):
        self.num_pages = int(input("Введите количество страниц для парсинга: "))

    def get_html(self, url, params=''):
        r = requests.get(url, headers=self.HEADERS, params=params)
        return r

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('section', class_="ticket-item")
        auto = []
        sleep(3)
        for item in items:
            auto.append(
                {
                    'title': item.find('div', class_='item ticket-title').get_text(strip=True),
                    'link-produt': self.HOST + item.find('div', class_='content-bar').find('a').get('href'),
                    'price': item.find('div', class_='price-ticket').get_text(strip=True),
                    'information': item.find('div', class_='base_information').get_text(strip=True),
                    'characteristic': item.find('div', class_='definition-data').find('ul',
                                                                                      class_="unstyle characteristic").get_text(
                        strip=True),
                    'foto': self.HOST + item.find('div', class_='content-bar').find('img').get('src')
                }
            )
        return auto

    def save_info(self, items, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['марка авто', 'ссылка на продукт', 'Цена', " Информация", "Данные номеров", "Изображение"])
            for item in items:
                writer.writerow(
                    [item['title'], item['link-produt'], item['price'], item['information'], item['characteristic'],
                     item['foto']])

    def show_total_count(self, items):
        print(f'Общее количество машин на выбранных страницах: {len(items)}')

    def run(self):
        html = self.get_html(self.URL)
        if html.status_code == 200:
            auto = []
            for page in range(1, self.num_pages + 1):
                print(f'Парсим страницу :  {page}')
                html = self.get_html(self.URL, params={'page': page})
                auto.extend(self.get_content(html.text))
                self.save_info(auto, self.CSV)
            self.show_total_count(auto)
            pass
        else:
            print('Error')


parser = AutoParser()
parser.run()









