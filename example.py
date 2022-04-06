from bs4 import BeautifulSoup
import requests
import csv


CSV = 'kivano.csv'
URL = 'https://www.kivano.kg/mobilnye-telefony'
HOST = 'https://www.kivano.kg/'


def get_html(URL, params = ''):
    r = requests.get(URL, params=params, verify=False)
    return r


def get_content(html):
    soup = BeautifulSoup(html)
    items = soup.find_all('div', class_='list-view')

    comps = []

    for item in items:
        comps.append({
            'name': item.find('div', class_='listbox_title').text.strip(),
            'price': item.find('div', class_='listbox_price').text.strip(),
            'link': HOST + item.find('div', class_='listbox_img').find('a').get('href'),
            'image': item.find('div', class_='listbox_img').find('img').get('src')
        })

    return comps


def save(items, path):
    with open(path, 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'price', 'link', 'image'])
        for item in items:
            writer.writerow([item['name'], item['price'], item['link'], item['image']])


def pagination():
    PAGINATION = input('items: ')
    PAGINATION = int(PAGINATION)
    html = get_html(URL)
    if html.status_code == 200:
        items = []
        for page in range(1, PAGINATION + 1):
            print(f'page {page} is done')
        html = get_html(URL, params={'page': page})
        items.extend(get_content(html.text))
        save(items, CSV)
        print('parsing is done')

    else:
        print('parsing is break')


pagination()