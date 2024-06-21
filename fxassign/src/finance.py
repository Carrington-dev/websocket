import random

# USD to EUR: 0.85
# EUR to GBP: 0.75
# GBP to USD: 1.20

class Finance:
    def generate(self, firstCurrency="USD", secondCurrency="EUR"):
        if firstCurrency == "USD" and secondCurrency == "EUR":
            return random.randint(84, 86) / 100
        if firstCurrency == "EUR" and secondCurrency == "GBP":
            return random.randint(74, 76) / 100
        if firstCurrency == "GBP" and secondCurrency == "USD":
            return random.randint(119, 121) / 100
        return