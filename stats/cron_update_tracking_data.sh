#!/bin/bash
now=$(date +"%D %T")
echo "Started update at $now"

echo 'Moving to working directory...'
cd /home/jgrizou/workspace/openvault_web/stats

echo 'Building database from logs...'
/home/jgrizou/miniconda3/envs/openvault_deploy/bin/python build_db.py

echo 'Building CSV from database...'
/home/jgrizou/miniconda3/envs/openvault_deploy/bin/python build_csv.py

echo 'Pushing CSV to google spreadsheet...'
/home/jgrizou/miniconda3/envs/openvault_deploy/bin/python push_to_google_sheet.py

now=$(date +"%D %T")
echo "Finished update at $now"
