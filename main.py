import requests
from bs4 import BeautifulSoup as BS
import lxml
import csv

# ФИО, фракция и номер телефона

url = 'http://kenesh.kg/ru/deputy/list/35'
page_count = 6

def open_page(url):
    # Принимает адрес страницы, открывает ее и возвращает содержимое страницы (html - код)
    response = requests.get(url)
    # print(response.status_code)
    # print(response.text)
    return response.text

def analyze_page_content(page_content):
    '''Принимает код страницы , анализирует его и подготавливает к получению данных'''
    soup = BS(page_content, 'lxml')
    return soup

def get_info(soup):
    listing = soup.find('div', class_ = 'grid-deputs')
    product_cards = listing.find_all('div', class_= 'dep-item')
    return product_cards

def get_some_data(info):
    try:
        name = info.find('a', class_='name').text .strip()
    except:
        name = 'Депутат'

    try:
        fraction = info.find('div', class_='info').text .strip()
    except:
        fraction = 'Какая-та фракция'

    try:
        phone = info.find('a', class_='phone-call').text.strip()
    except:
        phone = 'Какой-то телефон'

    return {'name': name, 'fraction': fraction, 'phone': phone}

def parse():
    all_main_info = []
    for page in range(1, page_count + 1):
        page_url = f'{url}?page={page}'
        content = open_page(page_url)
        soup = analyze_page_content(content)
        main_info = get_info(soup)
        all_main_info.extend(main_info)

    data = []
    for info in all_main_info:
        data.append(get_some_data(info))


    def write_to_csv(data):
        with open('deputies.csv', 'w') as file:
            columns = ['ФИО', 'Фракция', 'Телефон']
            writer = csv.DictWriter(file, columns)
            writer.writeheader()
            for member in data:
                writer.writerow({
                    'ФИО': member['name'],
                    'Фракция': member['fraction'],
                    'Телефон': member['phone']
                    })
    write_to_csv(data)

if __name__ == '__main__':
    parse()

print(f'Parsing is over')