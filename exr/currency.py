import requests
import json


def get_currency_of_country(country_code):
    url = "https://store.steampowered.com/api/appdetails?filters=price_overview&appids=427520&cc=" + country_code
    req = requests.get(url)
    data = req.content.decode(req.encoding)
    j = json.loads(data)
    try:
        currency = j[str(427520)]['data']['price_overview']['currency']
        return currency
    except:
        return "XXX"


def get_exchange_rate(c_from, c_to):
    url = 'https://api.frankfurter.app/latest?amount=1&from=' + c_from + '&to=' + c_to
    req = requests.get(url)
    data = req.content.decode(req.encoding)
    j = json.loads(data)
    try:
        exr = j['rates'][c_to]
        return exr
    except:
        return 0
