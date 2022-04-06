from bs4 import BeautifulSoup
import requests
import csv

CSV = 'kivano.csv'
URL = 'https://www.kivano.kg/noutbuki'
HOST = 'https://www.kivano.kg'


def get_html(URL, params = ''):
    r = requests.get(URL, params = params, verify = False)
    data = data.encode('UTF-8', 'ignore')
    return r


def get_content(html):
    soup = BeautifulSoup(html)
    items = soup.find_all('div', class_='list-view')
    laptops = []
    for item in items:
        laptops.append({
            'name': item.find('div', class_='listbox_title').text.strip(),
            'price': item.find('div', class_='listbox_price').text.strip(),
            'link': HOST + item.find('div', class_='listbox_img').find('a').get('href'),
            'image': item.find('div', class_='listbox_img').find('img').get('src')
        })
    return laptops


def save_file(items, path):
    with open(path,'w') as data_f:
        writer = csv.writer(data_f, delimiter=';')
        writer.writerow(['name', 'price', 'image', 'link'])
        for item in items:
            writer.writerow([item['name'], item['price'], item['image'], item['link']])


def get_page():
    PAGINATION = input('pages ? :')
    PAGINATION = int(PAGINATION.strip())
    items = []
    html = get_html(URL)
    if html.status_code == 200:
        for page in range(1, PAGINATION + 1):
            print(f'page {page} is done')
            html = get_html(URL, params={'pages': page})
            items.extend(get_content(html.text))
        save_file(items, CSV)
        print('Parsing finished')
    else:
        print('Parsing interrupted')
get_page()