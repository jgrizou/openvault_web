import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# see gspread setup here https://gspread.readthedocs.io/en/latest/oauth2.html
# pip install gspread
# pip install --upgrade oauth2client

import gspread
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FOLDERNAME = os.path.join(HERE_PATH, 'credentials')
CREDENTIALS_FILENAME = os.path.join(CREDENTIALS_FOLDERNAME, 'OPENVAULT-f5d955c41c20.json')

CSV_FOLDERNAME = os.path.join(HERE_PATH, 'csv')
CSV_FILENAME = os.path.join(CSV_FOLDERNAME, 'tracking_data.csv')

SPREADSHEET_ID = '1_eZhXE5kWl9tJaYAdPC-ZG3FqLMMYDfJR_rqlrHBv5A'


if __name__ == '__main__':

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILENAME, scope)

    gc = gspread.authorize(credentials)
    content = open(CSV_FILENAME, 'r').read().encode('utf-8')
    gc.import_csv(SPREADSHEET_ID, content)
