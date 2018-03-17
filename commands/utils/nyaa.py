from bs4 import BeautifulSoup
from urllib.parse import quote_plus

import requests


class Nyaa:
    def __init__(self, query):
        # creating the soup
        self._url = "https://nyaa.si/?f=0&c=0_0&q="\
                    f"{quote_plus(query, encoding='utf-8')}&s=seeders&o=desc"

        self._data = requests.get(self._url).text
        self._soup = BeautifulSoup(self._data, 'lxml')

        if 'comment' in self._soup.select('div.table-responsive td[colspan] a')[0]['title']:
            self.title = self._soup.select('div.table-responsive td[colspan] a')[1]['title']
            self.url = f"https://nyaa.si{self._soup.select('div.table-responsive td[colspan] a')[1]['href']}"
        else:
            self.title = self._soup.select('div.table-responsive td[colspan] a')[0]['title']
            self.url = f"https://nyaa.si{self._soup.select('div.table-responsive td[colspan] a')[0]['href']}"

        self.torrent = f"https://nyaa.si{self._soup.select('div.table-responsive td.text-center a')[0]['href']}"

        self.file_size = self._soup.select('div.table-responsive td')[3].text
        self.upload_date = self._soup.select('div.table-responsive td')[4].text
        self.seeders = self._soup.select('div.table-responsive td')[5].text
        self.leechers = self._soup.select('div.table-responsive td')[6].text
