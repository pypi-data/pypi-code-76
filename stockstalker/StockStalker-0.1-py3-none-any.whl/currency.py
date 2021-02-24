import requests
import json
import numpy as np

supportedCurrencies = []


def notValidCurrencyError():
    raise Exception(f"Currency not supported \n Supported currencies are: {supportedCurrencies}")

class Currency:
    def __init__(self, shorthand, amount):
        self.shorthand = shorthand
        self.amount = amount
        self.date = None

        if verifyShorthand(self.shorthand) == False:
            notValidCurrencyError()




def Convert(base, shorthandToConvert):


    if verifyShorthand(shorthandToConvert) == False:
        notValidCurrencyError()

    req = requests.get(f"https://api.exchangeratesapi.io/latest?base={base.shorthand}")
    data = req.json()

    converted = base.amount * data["rates"][shorthandToConvert]
    obj = Currency(shorthandToConvert, converted)
    obj.date = data["date"]

    return obj

def updateSupportedCurrencies():
    global supportedCurrencies

    supportedCurrencies = []

    req = requests.get("https://api.exchangeratesapi.io/latest")
    data = req.json()

    keys = data["rates"].keys()
    array = list(keys)

    for x in range(0, len(array)):
        supportedCurrencies.append(array[x])

    supportedCurrencies.append("EUR")

def verifyShorthand(toVerify):
    if toVerify in supportedCurrencies:
        return True
    else:
        return False



updateSupportedCurrencies()