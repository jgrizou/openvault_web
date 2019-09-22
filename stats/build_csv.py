import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from datetime import datetime

import pandas as pd
import tinydb

import tools

DB_FOLDERNAME = os.path.join(HERE_PATH, 'db')
TRACKING_DB_FILENAME = os.path.join(DB_FOLDERNAME, 'tracking_info.json')

CSV_FOLDERNAME = os.path.join(HERE_PATH, 'csv')
tools.ensure_dir(CSV_FOLDERNAME)

CSV_FILENAME = os.path.join(CSV_FOLDERNAME, 'tracking_data.csv')

UNKNOWN_REFERENCE = ''


def get_location_info(client_ip_info):

    location_info = {}

    # fill list with unknown values
    field_list = ['ip', 'country', 'region', 'city', 'geo']
    for field_name in field_list:
        location_info[field_name] = UNKNOWN_REFERENCE

    api_provider = item['client_ip_info']['api_provider']
    api_info = item['client_ip_info']['api_info']

    if api_provider == 'http://ip-api.com/':
        location_info['ip'] = api_info['query']
        if api_info['status'] == 'success':
            location_info['country'] = api_info['countryCode']
            location_info['region'] = api_info['regionName']
            location_info['city'] = api_info['city']
            location_info['geo'] = '{},{}'.format(api_info['lat'], api_info['lon'])

    elif api_provider == 'http://ipinfo.io':
        location_info['ip'] = api_info['ip']
        if api_info['ip'] != '127.0.0.1':
            location_info['country'] = api_info['country']
            location_info['region'] = api_info['region']
            location_info['city'] = api_info['city']
            location_info['geo'] = api_info['loc']

    return location_info


def get_referer_url(item):
    if 'url_info' in item:
        url_info = item['url_info']
        if url_info['referrer']:
            return url_info['referrer']
        else:
            return url_info['href']
    else:
        return UNKNOWN_REFERENCE


def get_config_type(config_filename):
    return config_filename.split('_')[0]


if __name__ == '__main__':

    db = tinydb.TinyDB(TRACKING_DB_FILENAME)

    tracking_df = pd.DataFrame()
    for item in db.__iter__():

        data = {}

        data['date'] = pd.to_datetime(datetime.fromtimestamp(item['timestamp']))

        data['event'] = 1  # just to count connection events

        data['user_platform'] = item['user_platform']
        data['user_browser'] = item['user_browser']
        data['pad_type'] = item['config']['pad']['type']
        data['config_filename'] = os.path.split(item['config_filename'])[1]
        data['config_type'] = get_config_type(data['config_filename'])

        location_info = get_location_info(item['client_ip_info'])
        data.update(location_info)

        data['referer_url'] = get_referer_url(item)

        # create DataFrame and append to current one
        tmp_df = pd.DataFrame(data, index=[0])
        tracking_df = tracking_df.append(tmp_df, ignore_index=True)

    # sort by date and save
    tracking_df = tracking_df.sort_values(by=['date'])
    tracking_df.to_csv(CSV_FILENAME, index=None)
