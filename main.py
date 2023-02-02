import requests
from bs4 import BeautifulSoup
import csv

CSV = 'auto.csv'
HOST = 'https://auto.ria.com/'
URL = 'https://auto.ria.com/uk/legkovie/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_="ticket-item")
    auto = []

    for item in items:
        auto.append(
        {
           'title': item.find('div', class_= 'item ticket-title').get_text(strip=True),
           'link-produt': HOST + item.find('div', class_='content-bar').find('a').get('href'),
            'price': item.find('div', class_='price-ticket').get_text(strip=True),
            'information': item.find('div', class_='base_information').get_text(strip=True),
            'characteristic': item.find('div', class_='definition-data').find('ul', class_= "unstyle characteristic").get_text(strip=True),
            'foto': HOST + item.find('div', class_='content-bar').find('img').get('src')
        }
    )
    return auto

def save_info(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['марка авто', 'ссылка на продукт', 'Цена', " Информация", "Данные номеров", "Изображение" ])
        for item in items:
            writer.writerow([item['title'], item['link-produt'], item['price'], item['information'], item[ 'characteristic' ], item['foto']])
def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        auto = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу :  {page}')
            html = get_html(URL, params={'page': page})
            auto.extend(get_content(html.text))
            save_info(auto, CSV)
        pass        #print(auto)
    else:
        print('Error')

parser()







