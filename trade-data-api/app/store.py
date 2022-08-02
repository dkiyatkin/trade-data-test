from random import random
from datetime import datetime, timezone


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


class TickerStore:
    def __init__(self):
        self.tickers = {}
        for i in range(100):
            ticker_id = "ticker_" + str(i).zfill(2)
            self.tickers[ticker_id] = [
                {"price": 0, "pos": 0, "date": datetime.now(timezone.utc)}
            ]

    async def generate_ticker_item(self, ticker_id):
        ticker = self.tickers.get(ticker_id)
        if ticker is None:
            return None
        prev_ticker_item = ticker[-1]
        next_ticker_item = {
            "price": prev_ticker_item["price"] + generate_movement(),
            "pos": prev_ticker_item["pos"] + 1,
            "date": datetime.now(timezone.utc),
        }
        if len(ticker) >= 3600:
            self.tickers[ticker_id] = ticker[1:]
            ticker = self.tickers[ticker_id]
        ticker.append(next_ticker_item)
        return next_ticker_item

    async def get_cur_tickers(self):
        cur_tickers = {}
        for ticker_id in self.tickers:
            cur_tickers[ticker_id] = self.tickers[ticker_id][-1]
        return cur_tickers

    async def get_ticker_ids(self):
        return list(self.tickers.keys())

    async def get_ticker(self, ticker_id: str):
        return self.tickers.get(ticker_id)
