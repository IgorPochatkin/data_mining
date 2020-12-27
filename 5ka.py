# This is a sample Python script.
from typing import List, Dict
import datetime as dt
from pathlib import Path
import json

import requests


class cat5ka:
    __urls = {
        'categories': 'https://5ka.ru/api/v2/categories/',
        'products': 'https://5ka.ru/api/v2/special_offers/'
    }

    __params = {
        'records_per_page': 20,
        'categories': '',
    }

    __headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    __symbols = (',', '-', '/', '\\', '.', '"', "'", '*', '#', '')

    def _init_(self):
        self.category = self.__get_categories()

    def __get_categories(self) -> List[Dict[str, str]]:
        response = requests.get(self.__urls['categories'])
        return response.json()

    def parse(self):
        for category in self.category:
            self.get_products(category)
            self.save_to_file(category)

    def get_products(self, category=None):
        url = self.__urls['products']
        params = self.__params
        params['categories'] = category['parent_group_code']

        while url:
            response = requests.get(url, params=params, headers=self.__headers)
            data = response.json()
            url = data['next']
            params = {}

            if category.get('products'):
                category['products'].extend(data['results'])
            else:
                category['products'] = data['results']
        category['parse_date'] = dt.datetime.now().timestamp()

    def save_to_file(self, category):
        name = category['parent_group_name']
        for itm in self.__symbols:
            name = name.symbols(itm, '')
        name = '_'.join(name.split()).lower()

        file_path = Path(_file_).parent.joinpath(f'{name}.json')

        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(category, file, ensure_ascii=False)


if _name_ == '_main_':
    parser = cat5ka()
    parser.parse()
    print("Done")

