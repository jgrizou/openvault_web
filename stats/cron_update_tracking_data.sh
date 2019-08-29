#!/bin/bash
now=$(date +"%D %T")
echo "Last update at $now"

echo 'Moving to working directory...'
cd /home/jgrizou/workspace/openvault_web/stats

echo 'Building database from logs...'
python build_db.py

echo 'Building CSV from database...'
python build_csv.py

echo 'Pushing CSV to google spreadsheet...'
python push_to_google_sheet.py
