import json
from django.contrib.staticfiles import finders


def load_config(app):
    config_path = finders.find('datas/' + str(app) + '-config.json')
    config_file = open(config_path, 'r')
    config = json.load(config_file)

    return config

