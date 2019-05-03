

## user

adduser --gecos "" jgrizou
usermod -aG sudo jgrizou

//create ssh key
ssh-keygen -t rsa -b 4096 -C "jonathan.grizou@gmail.com"
// add it to github

// allow ssh to jgrizou

$ echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCtwC4jo32WdRZlyfpErHo7Ro38tFNEuJ1+2U7XLqjhujHR0pZA9E8/aEZOJ+plFhXo5ojXsTCnWbwwS+JjGksbo7ebOfyNypN/Fr1xOJqIaK6YVR0WtNnMW+cnL5k6fv5bUpkCHzi0Pe8E787G0qk4ouefrueyPblOU2jpgyhuXPreTgz+8n2ho6KWLZSWrKNIpPgmsKJR9n/K78vvMBLEcWBxrnvb06kWvPFMIGEno3J19V/xrEoVF7keWpSYdlmhhb5/7ApiybwoZk4vqc85e6qwyzm8mcWZHFF7ASFdoy+1ZpQGIHx2nbsVs/ta9OTzjF7Io49ler4j3I+9fVwj jonathan.grizou@gmail.com >> ~/.ssh/authorized_keys
$ chmod 600 ~/.ssh/authorized_keys

// secure server_name

sudo nano /etc/ssh/sshd_config

-> PermitRootLogin no


$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw --force enable
$ sudo ufw status

$ sudo apt-get -y update
$ sudo apt-get -y install supervisor nginx

## miniconda3

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh

source ~/.bashrc
conda create --name openvault_deploy python=3.7

// add to bashrc for auto loading of env
echo "conda activate openvault_deploy" >> ~/.bashrc

//
pip install flask
pip install flask-socketio
pip install eventlet
pip install gunicorn

conda install -c conda-forge nodejs

conda install numpy
pip install sklearn


## flask

// create .env in flask server folder with SERVER_KEY

touch .env // in /home/jgrizou/workspace/openvault_rpi/app/server

// generate Secret Key
python3 -c "import uuid; print(uuid.uuid4().hex)"

echo "SECRET_KEY=135d12a08cae4b97aaf4148b67de4b3a" >> .env

//
echo "export FLASK_APP=app.py" >> ~/.profile


## App

git clone git@github.com:jgrizou/openvault.git
git clone git@github.com:jgrizou/openvault_rpi.git

// in openvault_rpi/app/client

npm install
npm run build

## supervisor config

sudo nano /etc/supervisor/conf.d/openvault.conf

```
[program:openvault]
command=/home/jgrizou/miniconda3/envs/openvault_deploy/bin/gunicorn -b localhost:8000 --worker-class eventlet -w 1 app:app
directory=/home/jgrizou/workspace/openvault_rpi/app/server
user=jgrizou
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

// --worker-class eventlet is for websocket
// -w 1 is for 1 worker but this is mandatory when using websocket

sudo supervisorctl tail openvault stdout

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

systemctl restart nginx
