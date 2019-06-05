import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import uuid
import time
import datetime

import json
import requests

import tools
import web_tools

LOG_FOLDER = os.path.join(HERE_PATH, 'logs')
MP3_FOLDER_NAME = 'mp3'
MAP_FOLDER_NAME = 'maps'


def generate_unique_log_folder():
    while True:
        log_folder = os.path.join(LOG_FOLDER, str(uuid.uuid4()))
        if not os.path.exists(log_folder):
            break
    tools.ensure_dir(log_folder)
    return log_folder


def get_ip_information(ip_address):
    api_url = 'http://ip-api.com/json/{}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,reverse,mobile,proxy,query'
    response = requests.get(api_url.format(ip_address))

    if response.ok:
        return json.loads(response.content)
    else:
        return {} # empty dict signify api call did not work properly

class Logger(object):

    def __init__(self):
        self.log_folder = generate_unique_log_folder()
        print('Starting Logger at {}'.format(self.log_folder))

    def log_new_connnection(self, client_ip, user_agent, room_id, config_filename, config):

        connection_info = {}

        connection_info['room_id'] = room_id
        connection_info['config_filename'] = config_filename
        connection_info['config'] = config

        connection_info['client_ip'] = client_ip
        connection_info['client_ip_info'] = get_ip_information(client_ip)

        if user_agent:
            connection_info['user_agent'] = user_agent.string
            connection_info['user_platform'] = user_agent.platform
            connection_info['user_browser'] = user_agent.browser

        timestamp = time.time()
        timestamp_human_readable = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S on %d/%m/%Y')
        connection_info['timestamp'] = timestamp
        connection_info['timestamp_human_readable'] = timestamp_human_readable

        connection_info_filename = os.path.join(self.log_folder, 'connection_info.json')
        tools.save_json(connection_info_filename, connection_info)


    def save_classifier_map_to_file(self, classifier_map):
        map_folder = os.path.join(self.log_folder, MAP_FOLDER_NAME)
        tools.ensure_dir(map_folder)

        files = tools.list_files(map_folder, ['*.png'])
        map_filename = os.path.join(map_folder, '{:04}.png'.format(len(files)))

        web_tools.save_map_to_file(classifier_map, map_filename)

        return map_filename


    def save_mp3_to_file(self, mp3_data):
        mp3_folder = os.path.join(self.log_folder, MP3_FOLDER_NAME)
        tools.ensure_dir(mp3_folder)

        files = tools.list_files(mp3_folder, ['*.mp3'])
        mp3_filename = os.path.join(mp3_folder, '{:04}.mp3'.format(len(files)))
        with open(mp3_filename, 'wb') as f:
            f.write(mp3_data)
        return mp3_filename
