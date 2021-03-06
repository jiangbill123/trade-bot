# we need to remove all the tickers that don't exist on robinhood and are priced below $1.5

import requests
import pandas as pd
from stock import Stock
import threading
from helper import get_tickers
from constants import FILTERED_TICKERS_FILEPATH, WATCHLIST_TICKERS_FILEPATH, MIN_PRICE, MIN_VOLUME

def analyze_stocks() -> None:
    """ analyze every ticker """
    print('starting analysis')
    tickers = get_tickers(FILTERED_TICKERS_FILEPATH)
    thread_list = []
    watchlist_stocks = []
    losing_stocks = []

    def check_blow(tkr: str) -> None:
        try:
            stock = Stock(tkr)
            if (stock.volume > stock.avg_volume * 2.5):
                watchlist_stocks.append(stock)
                print(stock)
            else:
                print(f'Skipping ${stock.ticker}')
        except Exception as e:
            print(tkr, e)

    for tkr in tickers:
        s_thread = threading.Thread(target=check_blow, args=(tkr,))
        s_thread.start()
        thread_list.append(s_thread)

    for thread in thread_list:
        thread.join()

    print('Here are today\'s blowing stocks')
    for stock in watchlist_stocks:
        print(stock)

    watchlist_tickers = [s.ticker for s in watchlist_stocks]
    prices = [s.price for s in watchlist_stocks]
    volumes = [s.volume for s in watchlist_stocks]
    avg_volumes = [s.avg_volume for s in watchlist_stocks]
    volume_dif_fractions = [s.volume_dif_fraction for s in watchlist_stocks]
    changes = [s.change for s in watchlist_stocks]
    overnight_changes = [s.overnight_change for s in watchlist_stocks]
    day_changes = [s.day_change for s in watchlist_stocks]

    df = pd.DataFrame(data={'ticker': watchlist_tickers, 'price': prices, 'volume': volumes, 'avg volume': avg_volumes,
                            'volume factor': volume_dif_fractions, 'change': changes, 'overnight change': overnight_changes, 'day change': day_changes})

    df.to_csv(WATCHLIST_TICKERS_FILEPATH, index=False)


if __name__ == '__main__':
    analyze_stocks()
    print('analysis complete')
