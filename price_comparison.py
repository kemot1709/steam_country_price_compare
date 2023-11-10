import json
import sys
import warnings
import pandas as pd
from pandas.errors import SettingWithCopyWarning

from steam.price import get_game_price, get_price_data
from steam.games import get_game_name, import_list_of_games, import_id_to_name_list
from exr.currency import get_currency_of_country, get_exchange_rate

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


def add_prices_to_table(pd_table, country, games):
    ret = get_price_data(country, games)
    j = json.loads(ret)
    pd_table['Price ' + country] = 0.0
    for row in pd_table.iterrows():
        pd_table['Price ' + country][row[0]] = get_game_price(j, row[1]['ID'])


if __name__ == "__main__":
    COUNTRY_A = sys.argv[1]
    COUNTRY_B = sys.argv[2]
    try:
        CONV_A_TO_B = float(sys.argv[3])
    except:
        CURR_A = get_currency_of_country(COUNTRY_A)
        CURR_B = get_currency_of_country(COUNTRY_B)
        CONV_A_TO_B = get_exchange_rate(CURR_A, CURR_B)

    app_list = import_id_to_name_list('data/id2name_list')
    games_id = import_list_of_games("data/list_of_apps")
    table = pd.DataFrame({'ID': games_id})

    table["Name"] = ''
    for row in table.iterrows():
        table['Name'][row[0]] = get_game_name(app_list, row[1]['ID'])

    add_prices_to_table(table, COUNTRY_A, games_id)
    add_prices_to_table(table, COUNTRY_B, games_id)
    table['Price converted ' + COUNTRY_A] = table['Price ' + COUNTRY_B] / CONV_A_TO_B
    table['Percent of price'] = (table['Price converted ' + COUNTRY_A] * 100.0 / table['Price ' + COUNTRY_A])

    # Drop free or badly imported games
    table.drop(table[table['Price ' + COUNTRY_A] == 0.0].index, inplace=True)
    table.drop(table[table['Price ' + COUNTRY_B] == 0.0].index, inplace=True)

    print(table['Percent of price'].mean())
    print(table.sort_values(by=['Percent of price'], ascending=True).to_string())
    pass
