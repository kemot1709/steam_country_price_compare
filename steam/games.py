import requests
import json
import os.path


def import_id_to_name_list(filename):
    if not os.path.isfile(filename):
        # Import list of games with its ID
        url = 'https://api.steampowered.com/ISteamApps/GetAppList/v0002/'
        req = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(req.content)

    with open(filename, encoding='utf-8') as json_file:
        app_list = json.load(json_file)
        return app_list


def import_list_of_games(filename):
    with open(filename) as file:
        data = file.read()
        data = data.replace('\n', '')
        games_id = data.split(',')
        return games_id


def get_game_name(app_list, game_id):
    for app in app_list['applist']['apps']:
        if app['appid'] == int(game_id):
            return app['name']
