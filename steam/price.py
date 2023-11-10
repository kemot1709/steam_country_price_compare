import requests
import json


def get_game_price(json_return, game_id):
    try:
        price = json_return[str(game_id)]['data']['price_overview']['final']
        return int(price) / 100.0
    except:
        return 0.0


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
