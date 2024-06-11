class ArbitrageDetector:
    def __init__(self, threshold=0.001):
        self.threshold = threshold

    def detect_arbitrage(self, data):
        opportunities = []
        for pair, prices in data.items():
            bid, ask = prices['bid'], prices['ask']
            spread = ask - bid
            if spread > self.threshold:
                opportunities.append((pair, spread))
        return opportunities
