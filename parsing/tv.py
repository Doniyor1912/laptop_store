import requests
from bs4 import BeautifulSoup

from data_base.tv_db import Postgresql_tv


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    main_block = soup.find('div', class_='proposal')
    product_block = main_block.find_all('div', class_="proposal-column")
    host1 = "https://glotr.uz"

    content = []
    for product in product_block:
        brand_name = product.find('span', class_="text-overflow-two-line").get_text(strip=True)
        product_image = product.find('a')['data-src']
        product_price = product.find("span", class_="proposal-price-value").get_text(strip=True).replace("000", "000 ") + " " + product.find("span", class_="proposal-price-currency").get_text(strip=True)
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
        self.URL = 'https://glotr.uz/uz/televizorlar/'
        self.HOST = 'https://glotr.uz/'
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
        Postgresql_tv().create_table()
        for data in content:
            Postgresql_tv().insert_data(*data.values())
print(Postgresql_tv().select_data())


