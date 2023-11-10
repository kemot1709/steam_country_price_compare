import requests
import json
import warnings
import math
import pandas as pd
from pandas.errors import SettingWithCopyWarning

COUNTRY_A = 'PL'
COUNTRY_B = 'TR'
CONV_A_TO_B = 6.66  # TR
# CONV_A_TO_B = 82.56  # AR
# CONV_A_TO_B = 22.05  # RU
# CONV_A_TO_B = 19.62  # IN
# CONV_A_TO_B = 5797.0  # VN
# CONV_A_TO_B = 0.24  # USD (GE, US, NP, etc.)
# CONV_A_TO_B = 8.65  # UA
# CONV_A_TO_B = 112.51  # KZ
# CONV_A_TO_B = 1.13  # MY
# CONV_A_TO_B = 1.73  # CN

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# List from this site
# https://api.steampowered.com/ISteamApps/GetAppList/v0002/
with open('id2name_list', encoding='utf-8') as json_file:
    app_list = json.load(json_file)


def get_game_name(game_id):
    for app in app_list['applist']['apps']:
        if app['appid'] == int(game_id):
            return app['name']


def get_game_price(json_return, game_id):
    try:
        price = json_return[str(game_id)]['data']['price_overview']['final']
        return int(price) / 100.0
    except:
        return 0.0


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


def get_price_data(coutry_code, list_of_games):
    # Steam can't handle too long requests so i cut them to 100 games
    if len(list_of_games) > 100:
        cnt = int(len(list_of_games) / 100)
        if len(list_of_games) % 100 == 0:
            cnt -= 1

        string = ''
        for i in range(1, cnt):
            pom = list_of_games[(i - 1) * 100:i * 100]
            ret = get_price_data(coutry_code, pom)
            string += ret[1:-1] + ','
        ret = get_price_data(coutry_code, list_of_games[cnt * 100:])
        string += ret[1:-1]
        if string[-1] == ',':
            string = string[:-1]
        return '{' + string + '}'

    games_str = ''
    for game in list_of_games:
        games_str += str(game)
        games_str += ','
    url = 'https://store.steampowered.com/api/appdetails?filters=price_overview&appids=' + games_str + '&cc=' + coutry_code
    req = requests.get(url)
    return req.content.decode(req.encoding)


def import_list_of_games(filename):
    with open(filename)as file:
        data = file.read()
        data = data.replace('\n', '')
        games_id = data.split(',')
        return games_id


if __name__ == "__main__":
    games_id = import_list_of_games("list_of_apps")
    table = pd.DataFrame({'ID': games_id})

    # CURR_A = 'PLN'
    # CURR_B = 'TRY'

    CURR_A = get_currency_of_country('PL')
    CURR_B = get_currency_of_country('TR')

    table["Name"] = ''
    for row in table.iterrows():
        table['Name'][row[0]] = get_game_name(row[1]['ID'])

    ret = get_price_data(COUNTRY_A, games_id)
    j = json.loads(ret)
    table['Cena ' + COUNTRY_A] = 0.0
    for row in table.iterrows():
        table['Cena ' + COUNTRY_A][row[0]] = get_game_price(j, row[1]['ID'])

    ret = get_price_data(COUNTRY_B, games_id)
    j = json.loads(ret)
    table['Cena ' + COUNTRY_B] = 0.0
    for row in table.iterrows():
        table['Cena ' + COUNTRY_B][row[0]] = get_game_price(j, row[1]['ID'])

    CONV_A_TO_B = get_exchange_rate(CURR_A, CURR_B)
    table['Cena konwertowana ' + COUNTRY_A] = table['Cena ' + COUNTRY_B] / CONV_A_TO_B

    table['Discount'] = 100.0 - (table['Cena konwertowana ' + COUNTRY_A] * 100.0 / table['Cena ' + COUNTRY_A])

    # Drop free or badly imported games
    table.drop(table[table['Cena ' + COUNTRY_A] == 0.0].index, inplace=True)
    table.drop(table[table['Cena ' + COUNTRY_B] == 0.0].index, inplace=True)

    print(table['Discount'].mean())
    print(table.sort_values(by=['Cena konwertowana ' + COUNTRY_A], ascending=True).to_string())
    pass
