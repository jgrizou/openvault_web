#!/bin/bash

echo 'Building database from logs...'
python build_db.py

echo 'Building CSV from database...'
python build_csv.py

echo 'Pushind CSV to google spreadsheet...'
python push_to_google_sheet.py
