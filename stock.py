import time
from typing import Optional

import requests
from bs4 import BeautifulSoup


MIN_FRACTION_BLOWING = .5


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker

        self.__time = time.time()

        self.price = None
        self.open_price = None
        self.volume = None
        self.avg_volume = None
        self.change = None
        self.load_data()

    def load_data(self):
        self.__time = time.time()
        yahoo_result = requests.get("https://finance.yahoo.com/quote/" + self.ticker)
        self.print_time_dif('yahoo')
        robin_result = requests.get('https://robinhood.com/stocks/' + self.ticker)
        self.print_time_dif('robin hood')

        yahoo_c = yahoo_result.content
        robin_c = robin_result.content

        yahoo_soup = BeautifulSoup(yahoo_c, features="html.parser")
        robin_soup = BeautifulSoup(robin_c, features="html.parser")

        # for debugging
        #print(robin_soup.find_all(attrs={"class": "QzVHcLdwl2CEuEMpTUFaj"}))
        #print(robin_soup.find_all(attrs={"class": "QzVHcLdwl2CEuEMpTUFaj"})[0])
        #print(robin_soup.find_all(attrs={"class": "QzVHcLdwl2CEuEMpTUFaj"})[0].text)
        #print(robin_soup.find_all(attrs={"class": "QzVHcLdwl2CEuEMpTUFaj"})[0].text.replace(',', ''))

        self.price = float(robin_soup.find_all(
            attrs={"class": "QzVHcLdwl2CEuEMpTUFaj"})[0].text.replace(',', '')[1:])
        self.open_price = float(yahoo_soup.find_all(
            attrs={"data-test": "OPEN-value"})[0].text.replace(',', ''))
        self.volume = int(yahoo_soup.find_all(
            attrs={"data-test": "TD_VOLUME-value"})[0].text.replace(',', ''))
        self.avg_volume = int(yahoo_soup.find_all(
            attrs={"data-test": "AVERAGE_VOLUME_3MONTH-value"})[0].text.replace(',', ''))
        self.change = (self.price - self.open_price) * 100/self.open_price

    def is_blowing(self):
        """ If the current volume is above the average volume by enough then the stock is considered 'blowing' """
        return (self.volume - self.avg_volume) / self.avg_volume > MIN_FRACTION_BLOWING

    def print_time_dif(self, title: Optional[str] = ''):
        print(title, 'time (s):', time.time() - self.__time)
        self.__time = time.time()

    def __str__(self):
        return '\n' + '\n\t'.join((f'{key}: {value}' for key, value in vars(self).items() if not key.startswith('_'))) + '\n'


if __name__ == '__main__':
    kodk = Stock('kodk')
    print(kodk)
