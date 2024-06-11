import random
import time
import threading

class MarketDataFeed:
    def __init__(self):
        self.data = {}
        self.subscribers = []

    def generate_data(self):
        pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD']
        while True:
            for pair in pairs:
                bid = round(random.uniform(1.1, 1.5), 4)
                ask = bid + round(random.uniform(0.0001, 0.0005), 4)
                self.data[pair] = {'bid': bid, 'ask': ask, 'timestamp': time.time()}
            self.notify_subscribers()
            time.sleep(1)  # Update rates every second

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify_subscribers(self):
        for callback in self.subscribers:
            callback(self.data)
