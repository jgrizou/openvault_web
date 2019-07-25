# mostly from flask-mega-turorial

// first ssh in as a root user
ssh root@serverip

## user
// we want to setup our own user to avoid direct root access and limit access if needed

adduser --gecos "" jgrizou
usermod -aG sudo jgrizou

//logging as jgrizou
su jgrizou

//create ssh key
ssh-keygen -t rsa -b 4096 -C "jonathan.grizou@gmail.com"
// add it to github

// allow ssh to jgrizou
$ echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCtwC4jo32WdRZlyfpErHo7Ro38tFNEuJ1+2U7XLqjhujHR0pZA9E8/aEZOJ+plFhXo5ojXsTCnWbwwS+JjGksbo7ebOfyNypN/Fr1xOJqIaK6YVR0WtNnMW+cnL5k6fv5bUpkCHzi0Pe8E787G0qk4ouefrueyPblOU2jpgyhuXPreTgz+8n2ho6KWLZSWrKNIpPgmsKJR9n/K78vvMBLEcWBxrnvb06kWvPFMIGEno3J19V/xrEoVF7keWpSYdlmhhb5/7ApiybwoZk4vqc85e6qwyzm8mcWZHFF7ASFdoy+1ZpQGIHx2nbsVs/ta9OTzjF7Io49ler4j3I+9fVwj jonathan.grizou@gmail.com >> ~/.ssh/authorized_keys
$ chmod 600 ~/.ssh/authorized_keys

// test by trying to ssh directly as jgrizou

ssh jgrizou@serverip


// secure server for no root login
sudo nano /etc/ssh/sshd_config
-> PermitRootLogin no



// more security for allowing only specific connection

$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow from 127.0.0.1 to any port 5001 # this is for docker in audio embedding
$ sudo ufw --force enable
$ sudo ufw status numbered

// if need to delete a rule
// $ sudo ufw delete 0

// server is ready quite secured now in terms of incoming connection

## update server

$ sudo apt-get -y update
$ sudo apt-get -y upgrade

$ sudo apt-get -y install supervisor nginx


## pull al repos

mkdir workspace
cd workspace

git clone git@github.com:jgrizou/openvault.git
git clone git@github.com:jgrizou/openvault_web.git
git clone git@github.com:jgrizou/audio_features.git
git clone git@github.com:jgrizou/sketch_features.git



## python dependencies with miniconda3

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh
(optional: rm Miniconda3-latest-Linux-x86_64.sh)

// get conda on the command line now
source ~/.bashrc

// create a dedicated environement
conda create --name openvault_deploy python=3.7

// add to bashrc for auto loading of env
echo "conda activate openvault_deploy" >> ~/.bashrc

// test if it works
source ~/.bashrc  (should activate the openvault_deploy environement)

// webstuff
conda install -c conda-forge nodejs

pip install flask
pip install flask-socketio
pip install eventlet
pip install gunicorn
pip install requests

// math stuff
conda install numpy
conda install scipy
conda install scikit-learn
conda install -c conda-forge matplotlib

// audio stuff
pip install docker
conda install -c conda-forge umap-learn
conda install -c conda-forge librosa
conda install -c roebel pysndfile

## install docker and test audio feature embedding extractor

https://www.digitalocean.com/community/tutorials/comment-installer-et-utiliser-docker-sur-ubuntu-18-04-fr

// check docker is running
sudo systemctl status docker

// remember to add yourself to the docker group
sudo usermod -a -G docker $USER

// might need a reboot here if you encounter "docker: Got permission denied"
sudo reboot

// check if you can load max-audio-embedding-generator
docker pull codait/max-audio-embedding-generator

// for full test
docker run -it -p 5000:5000 codait/max-audio-embedding-generator

// the python side will need a backend to handle codec, installing ffmpeg does the job. librosa could raise raise NoBackendError() otherwise
sudo apt-get install ffmpeg

## flask setting

// create .env in flask server folder with SERVER_KEY

touch .env // in /home/jgrizou/workspace/openvault_web/server

// generate Secret Key
python -c "import uuid; print(uuid.uuid4().hex)"

echo "SECRET_KEY=CODERETURNEDBYABOVECOMMAND" >> .env

// set FLASK_APP in ~/.profile
echo "export FLASK_APP=$HOME/workspace/openvault_web/server/app.py" >> ~/.profile


## Client build

// in openvault_web/app/client

npm install
npm run build

## try that it works ok and develop

// we will run gunicorn on port 5000

// allow connection to port 5000
$ sudo ufw allow 5000
$ sudo ufw --force enable

// remember to change the websocket port in client/src/main.js to SERVERIP:5000

cd /home/jgrizou/workspace/openvault_web/server
/home/jgrizou/miniconda3/envs/openvault_deploy/bin/gunicorn --bind 0.0.0.0:5000 --capture-output --worker-class eventlet -w 1 app:app

// then connect to SERVERIP:5000, logs should display on your terminal

// remenber to delete ufw rules once disconnect

$ sudo ufw status numbered
$ sudo ufw delete 0INDEXTODELETE
$ sudo ufw --force enable

## supervisor config

sudo nano /etc/supervisor/conf.d/openvault.conf

```
[program:openvault]
command=/home/jgrizou/miniconda3/envs/openvault_deploy/bin/gunicorn --bind localhost:8000 --capture-output --log-level info --worker-class eventlet -w 1 app:app
directory=/home/jgrizou/workspace/openvault_web/server
user=jgrizou
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

// --worker-class eventlet is for websocket
// -w 1 is for 1 worker but this is mandatory when using websocket

sudo supervisorctl tail openvault stdout
sudo supervisorctl tail -f openvault stdout
sudo supervisorctl restart openvault
sudo supervisorctl stop openvault
sudo supervisorctl start openvault


systemctl status supervisor
systemctl stop supervisor
systemctl start supervisor
systemctl restart supervisor


## NGINX

sudo rm /etc/nginx/sites-enabled/default

sudo nano /etc/nginx/sites-enabled/openvault

```
server {
    # listen on port 80 (http)
    listen 80;
    server_name _;

    # write access and error logs to /var/log
    access_log /var/log/openvault_access.log;
    error_log /var/log/openvault_error.log;

    #this where socket io will be handling the request
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }

    location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://127.0.1:8000/socket.io;
    }

}
```

sudo service nginx reload

systemctl status nginx
systemctl restart nginx


## SSL certificate with lets-encrypt
// needed for voice audio level to work

https://blog.miguelgrinberg.com/post/running-your-flask
https://letsencrypt.org/
https://certbot.eff.org/

// first you need your dns to be properly configure so your domain name points to the correct ip

// certbot will communicate with let's encrypt and check we really own the website

install certbot: https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx


// use the installer for nginx
sudo certbot certonly --nginx

// This will create the certificates
Your certificate and chain have been saved at: /etc/letsencrypt/live/openvault.jgrizou.com/fullchain.pem
Your key file has been saved at: /etc/letsencrypt/live/openvault.jgrizou.com/privkey.pem

 // enable port 443 for https
 sudo ufw allow https
 sudo ufw --force enable
 sudo ufw status numbered

 // change websocket endpoint in client/src/main.js to https
 Vue.use(new VueSocketIO({
   debug: false,
   connection: 'https://openvault.jgrizou.com'
 }))

// test locally with sudo to access the .pem files
// remember to kill supervisord openvault process before: sudo supervisorctl stop openvault


sudo /home/jgrizou/miniconda3/envs/openvault_deploy/bin/gunicorn --capture-output --worker-class eventlet -w 1 --bind 0.0.0.0:5000 --certfile /etc/letsencrypt/live/openvault.jgrizou.com/fullchain.pem --keyfile /etc/letsencrypt/live/openvault.jgrizou.com/privkey.pem app:app


// make nginx manage https in the reverse proxy


sudo nano /etc/nginx/sites-enabled/openvault

```
server {

    # listen on port 443 (https)
    listen 443 ssl;
    server_name openvault.jgrizou.com;
    ssl_certificate /etc/letsencrypt/live/openvault.jgrizou.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/openvault.jgrizou.com/privkey.pem;

    # write access and error logs to /var/log
    access_log /var/log/openvault_access.log;
    error_log /var/log/openvault_error.log;

    #this where socket io will be handling the request
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }

    location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://127.0.1:8000/socket.io;
    }

}

server {

  # listen on port 80 (http)
  listen 80;
  server_name openvault.jgrizou.com;
  # redirect all http to https
  location / {
      return 301 https://$host$request_uri;
  }

}
```

sudo service nginx reload



// test gunicorn alone without supervisord, not need to https as this is internal to the server, nginx is handling the https

/home/jgrizou/miniconda3/envs/openvault_deploy/bin/gunicorn --bind localhost:8000 --capture-output --log-level info --worker-class eventlet -w 1 app:app

// no need to change any supervisor config simply start openvault again
sudo supervisorctl start openvault


# renew certificate

This is automatic with certbot but you should check

// make sure the certificate will be updated automatically when needed
// check in less /etc/cron.d/certbot if certbot is being executed at regular intervals

//Then run a dry run to check it is all ok
sudo certbot renew --dry-run
