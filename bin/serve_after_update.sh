#!/bin/bash

echo('Moving to client folder...')
cd /home/jgrizou/workspace/openvault_web/client
echo('Building the front end...')
npm run build
echo('Restarting the python server...')
sudo supervisorctl restart openvault
echo('Restarting the nginx server...')
sudo service nginx reload
echo('Last update is online now!')
