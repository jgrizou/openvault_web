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
MP3_FOLDERNAME = 'mp3'
MAP_FOLDERNAME = 'maps'
DRAWING_FOLDERNAME = 'drawings'
LEARNER_LOGS_FOLDERNAME = 'learner_logs'


def generate_unique_log_folder():
    while True:
        log_folder = os.path.join(LOG_FOLDER, str(uuid.uuid4()))
        if not os.path.exists(log_folder):
            break
    tools.ensure_dir(log_folder)
    return log_folder


IP_API_PROVIDERS = []
IP_API_PROVIDERS.append(('http://ip-api.com/', 'http://ip-api.com/json/{}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,reverse,mobile,proxy,query'))
IP_API_PROVIDERS.append(('http://ipinfo.io', 'http://ipinfo.io/{}/json'))
IP_API_PROVIDERS.append(('https://ipapi.co', 'https://ipapi.co/{}/json'))

## use following command to test the response time of an log_app_info
## curl https://ipinfo.io/24.48.0.1 -w %{time_connect}:%{time_starttransfer}:%{time_total}

def request_ip_information(request_url, timeout):

    try:
        response = requests.get(request_url, timeout=timeout)

        if response.ok:
            return response.json()
        else:
            tools.log_app_info('Response status {} in IP API call: {}'.format(response.status_code, request_url))
            return {} # empty dict signify api call did not work properly

    except Exception as e:
        tools.log_app_info('Error {} in IP API call: {}'.format(e, request_url))
        return {} # empty dict signify api call did not work properly


def get_ip_information(ip_address, timeout=0.5):

    for api_provider, blank_request in IP_API_PROVIDERS:

        request_url = blank_request.format(ip_address)
        api_info = request_ip_information(request_url, timeout=timeout)

        if api_info:
            tools.log_app_info('IP API success from {}'.format(api_provider))

            ip_information = {}
            ip_information['api_provider'] = api_provider
            ip_information['api_info'] = api_info
            return ip_information

        else:
            tools.log_app_info('IP API request failed for {}'.format(request_url))

    tools.log_app_info('All IP API call failed!')
    return {}

class Logger(object):

    def __init__(self):
        self.log_folder = generate_unique_log_folder()

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

    def log_url_info(self, url_info):
        url_info_filename = os.path.join(self.log_folder, 'url_info.json')
        tools.save_json(url_info_filename, url_info)

    def save_learner_logs_to_file(self, learner_logs):
        learner_logs_folder = os.path.join(self.log_folder, LEARNER_LOGS_FOLDERNAME)
        tools.ensure_dir(learner_logs_folder)

        files = tools.list_files(learner_logs_folder, ['*.json'])
        learner_logs_filename = os.path.join(learner_logs_folder, '{:04}.json'.format(len(files)))

        tools.save_json(learner_logs_filename, learner_logs)

        return learner_logs_filename


    def save_classifier_map_to_file(self, classifier_map):
        map_folder = os.path.join(self.log_folder, MAP_FOLDERNAME)
        tools.ensure_dir(map_folder)

        files = tools.list_files(map_folder, ['*.png'])
        map_filename = os.path.join(map_folder, '{:04}.png'.format(len(files)))

        web_tools.save_map_to_file(classifier_map, map_filename)

        return map_filename


    def save_mp3_to_file(self, mp3_data):
        mp3_folder = os.path.join(self.log_folder, MP3_FOLDERNAME)
        tools.ensure_dir(mp3_folder)

        files = tools.list_files(mp3_folder, ['*.mp3'])
        mp3_filename = os.path.join(mp3_folder, '{:04}.mp3'.format(len(files)))
        with open(mp3_filename, 'wb') as f:
            f.write(mp3_data)
        return mp3_filename


    def save_drawing_to_file(self, drawing_data):
        drawing_folder = os.path.join(self.log_folder, DRAWING_FOLDERNAME)
        tools.ensure_dir(drawing_folder)

        drawing_files = tools.list_files(drawing_folder, ['*.json'])
        drawing_filename = os.path.join(drawing_folder, '{:04}.json'.format(len(drawing_files)))
        tools.save_json(drawing_filename, drawing_data)

        return drawing_filename
