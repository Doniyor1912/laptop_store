import requests
from bs4 import BeautifulSoup

from data_base.laptop_db import Postgresql_laptop


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    main_block = soup.find('div', class_='products-box')
    product_block = main_block.find_all('div', class_="col-3")
    host1 = "https://texnomart.uz/"

    content = []
    for product in product_block:
        brand_name = product.find('h2').get_text(strip=True)
        product_image = product.find('img')["data-src"]
        product_price = product.find("div", class_="product-price__current").get_text(strip=True).replace("000", "000 ")
        product_url = host1 + product.find("a")['href']


        content.append({
            "brand_name": brand_name,
            "product_url": product_url,
            "product_image": product_image,
            "product_price": product_price,
        })
    return content


class Parser:
    def __init__(self):
        self.URL = 'https://texnomart.uz/uz/katalog/noutbuki/'
        self.HOST = 'https://texnomart.uz/'
        self.HEADERS = {"user-agent":
"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        }

    def get_html(self, url):
        response = requests.get(url, headers=self.HEADERS)
        try:
            response.raise_for_status()
            return response.text
        except requests.HTTPError:
            print(f'Ошибка {response.status_code}')

    def run(self):
        html = self.get_html(self.URL)
        content = get_content(html)
        Postgresql_laptop().create_table()
        for data in content:
            Postgresql_laptop().insert_data(*data.values())


