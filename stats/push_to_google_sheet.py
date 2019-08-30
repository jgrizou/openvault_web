import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import pandas as pd


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

    # previous version was using the import_csv function from gspread but this was conflicting tiwht google studio as it seems to delete the spreadsheet sheets and create a new one each time, breaking links internal to google studio. We use a batch cells approach now, which works. Reminder of old methods below:
    # content = open(CSV_FILENAME, 'r').read().encode('utf-8')
    # gc.import_csv(SPREADSHEET_ID, content)

    # load csv file
    df = pd.read_csv(CSV_FILENAME)

    cells = []
    # https://github.com/burnash/gspread/issues/515
    for n_column, header in enumerate(df.keys()):
        # first row is header
        cells.append(gspread.Cell(1, n_column + 1, header))
        for n_row, value  in enumerate(df[header]):

            if pd.isna(value):
                value = ''
            else:
                value = str(value)

            cells.append(gspread.Cell(n_row + 2, n_column + 1, value))

    # the size of the dataset can only increase in theory using current pipeline so we do not bother looking into the spreadsheet, etc, we just overwrite

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILENAME, scope)

    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)

    worksheet = sh.get_worksheet(0)
    worksheet.update_cells(cells)
