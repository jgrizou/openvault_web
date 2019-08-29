import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import tinydb

import tools

DB_FOLDERNAME = os.path.join(HERE_PATH, 'db')
tools.ensure_dir(DB_FOLDERNAME)

TRACKING_DB_FILENAME = os.path.join(DB_FOLDERNAME, 'tracking_info.json')
PROCESSED_DB_FILENAME = os.path.join(DB_FOLDERNAME, 'log_processed.json')

CONNECTION_INFO_FILENAME = 'connection_info.json'
URL_INFO_FILENAME = 'url_info.json'


# LOG_ROOT_FOLDER = os.path.join(HERE_PATH, 'logs')
LOG_ROOT_FOLDER = os.path.join(HERE_PATH, '../server/logs') ## for local server log build

if __name__ == '__main__':

    tracking_info_db = tinydb.TinyDB(TRACKING_DB_FILENAME)
    log_processed_db = tinydb.TinyDB(PROCESSED_DB_FILENAME)

    log_folders = tools.list_folders(LOG_ROOT_FOLDER)
    for log_folder in log_folders:

        tracking_info = {}

        log_folder_item = {os.path.split(log_folder)[1]: True}
        # if NOT processed, process it
        if log_folder_item not in log_processed_db:

            connection_file = os.path.join(log_folder, CONNECTION_INFO_FILENAME)
            url_file = os.path.join(log_folder, URL_INFO_FILENAME)

            if os.path.exists(connection_file):
                connection_info = tools.read_json(connection_file)
                tracking_info = connection_info

            if os.path.exists(url_file):
                url_info = tools.read_json(url_file)
                tracking_info['url_info'] = url_info

            if tracking_info in tracking_info_db:
                print('Skipping {}'.format(log_folder))
            else:
                print('Adding {}'.format(log_folder))
                tracking_info_db.insert(tracking_info)
                log_processed_db.insert(log_folder_item)
