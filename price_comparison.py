import requests
import json
import sys
import warnings
import math
import pandas as pd
from pandas.errors import SettingWithCopyWarning

from steam.price import get_game_price, get_price_data
from steam.games import get_game_name, import_list_of_games, import_id_to_name_list
from exr.currency import get_currency_of_country, get_exchange_rate

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

if __name__ == "__main__":
    COUNTRY_A = sys.argv[1]
    COUNTRY_B = sys.argv[2]
    try:
        CONV_A_TO_B = float(sys.argv[3])
    except:
        CURR_A = get_currency_of_country(COUNTRY_A)
        CURR_B = get_currency_of_country(COUNTRY_B)
        CONV_A_TO_B = get_exchange_rate(CURR_A, CURR_B)

    games_id = import_list_of_games("data/list_of_apps")
    table = pd.DataFrame({'ID': games_id})

    app_list = import_id_to_name_list('data/id2name_list')

    table["Name"] = ''
    for row in table.iterrows():
        table['Name'][row[0]] = get_game_name(app_list, row[1]['ID'])

    ret = get_price_data(COUNTRY_A, games_id)
    j = json.loads(ret)
    table['Price ' + COUNTRY_A] = 0.0
    for row in table.iterrows():
        table['Price ' + COUNTRY_A][row[0]] = get_game_price(j, row[1]['ID'])

    ret = get_price_data(COUNTRY_B, games_id)
    j = json.loads(ret)
    table['Price ' + COUNTRY_B] = 0.0
    for row in table.iterrows():
        table['Price ' + COUNTRY_B][row[0]] = get_game_price(j, row[1]['ID'])

    table['Price converted ' + COUNTRY_A] = table['Price ' + COUNTRY_B] / CONV_A_TO_B

    table['Discount'] = 100.0 - (table['Price converted ' + COUNTRY_A] * 100.0 / table['Price ' + COUNTRY_A])

    # Drop free or badly imported games
    table.drop(table[table['Price ' + COUNTRY_A] == 0.0].index, inplace=True)
    table.drop(table[table['Price ' + COUNTRY_B] == 0.0].index, inplace=True)

    print(table['Discount'].mean())
    print(table.sort_values(by=['Price converted ' + COUNTRY_A], ascending=True).to_string())
    pass
