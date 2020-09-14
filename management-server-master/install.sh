#!/bin/bash
echo "starting installations"
apt-get update
echo "installing postgres db"
apt-get -y install postgresql postgresql-contrib postgresql-server-dev-all libpq-dev
echo "postgres installed"
sudo -i -u postgres psql << EOF
CREATE DATABASE iptv;
create user iptvuser with encrypted password 'newpassword';
grant all privileges on database iptv to iptvuser;
EOF
echo "User created, installing python and apache server"
sudo add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get -y install python3-pip python3.8 apache2 libapache2-mod-wsgi-py3
pip3 install --upgrade pip
echo "installing virtuaenv"
pip3 install virtualenv
echo "setting up virtual env"
virtualenv venv
source venv/bin/activate
echo "install dependencies"
pip3 install -r requirements.txt
chmod -R 777 .
cp iptv.conf /etc/apache2/sites-available/
#echo "start app"
#python3 manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py runserver 0.0.0.0:8000 &
#python3 manage.py createcachetable
