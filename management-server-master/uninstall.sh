#!/bin/bash
echo "starting uninstallations"
echo "stopping service"
PY=`ps -aux | grep py | grep 0.0.0.0:8000 | awk {'print $2'}`
if [ ! -z "$PY" ]
then
       kill -9 $PY
fi
APACHE=`a2query -s | awk {'print $1".conf"'}`
if [ ! -z "$APACHE" ]
then
    a2dissite $APACHE
    systemctl reload APACHE2
fi
echo "stopping postgres db"
sudo su postgres /usr/lib/postgresql/10/bin/pg_ctl stop -D /var/lib/postgresql/10/main/
echo "removing codes"
rm -rf /var/log/streams
rm -rf /opt/stream
rm -rf ~/archive*
rm -rf ~/transcoder*
rm -rf ~/stream*
rm -rf /var/www/html/manage*
rm -rf /var/www/html/trans*
rm -rf /var/www/html/stream*
rm -rf /var/www/html/arch*
rm -rf /etc/apache2/sites-available/*
rm -rf /etc/apache2/sites-enabled/*

# remove apache websites
echo "removing database"
sudo su postgres psql << EOF
DROP DATABASE IF EXISTS IPTV;
DROP DATABASE IF EXISTS STREAMER;
DROP DATABASE IF EXISTS ARCHIVE;
DROP DATABASE IF EXISTS TRANSCODER;
EOF

POSTGRES_V=`pg_lsclusters | awk 'NR>1 {print $1}'`
sudo systemctl stop postgresql*
sudo pg_dropcluster --stop $POSTGRES_V main
apt-get --purge remove postgresql\*
rm -r /etc/postgresql/
rm -r /etc/postgresql-common/
rm -r /var/lib/postgresql/
userdel -r postgres
groupdel postgres

echo "uninstalling dependencies"
apt-get -y remove postgresql postgresql-contrib postgresql-server-dev-all libpq-dev
apt-get -y remove ffmpeg 