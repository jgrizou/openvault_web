
pip install pandas
pip install gspread
pip install --upgrade oauth2client


# test it works

./cron_update_tracking_data.sh


# add to cron


crontab -e

add the following cron task (see https://crontab-generator.org)

0 * * * * /home/jgrizou/workspace/openvault_web/stats/cron_update_tracking_data.sh > /home/jgrizou/workspace/openvault_web/stats/cron_logs.txt 2>&1
