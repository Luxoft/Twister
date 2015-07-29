#!/usr/bin/env bash

# if the machine is behind a proxy server, the http_proxy and https_proxy
# must be set
# replace username, password, proxy_server and proxy_port with valid ones
# and comment out the following couple of lines
# export http_proxy="http://<username>:<password>@<proxy_server>:<proxy_port>/"
# export https_proxy="http://<username>:<password>@<proxy_server>:<proxy_port>/"


# install git and a few dependencies
apt-get update
apt-get install -y git
apt-get install -y python-pip
apt-get install -y python-dev
apt-get install -y unzip

# install mysql server; the prompt for password must not be displayed
export DEBIAN_FRONTEND=noninteractive
apt-get -q -y install mysql-server

# install Apache
apt-get install -y apache2
apt-get remove python-lxml

# add username user
mkdir /home/user
useradd -d /home/user -s /bin/bash user
chown -R user:user /home/user
echo "user:password" | chpasswd

# download Twister from github as zip archive
wget https://github.com/Luxoft/Twister/archive/git_hub_branch.zip

# unzip Twister archive and try to install the server
unzip git_hub_branch.zip
cd Twister-git_hub_branch/installer
python install_dependencies.py
python installer_server.py --default
cd /opt/twister/bin
./start_server &

# copy the Twister GUI to /var/www
cd /home/vagrant/Twister-git_hub_branch/binaries/applet
cp * /var/www

# create the twister_demo database  and the user 'user'
cd /home/vagrant/Twister-git_hub_branch/installer/packages
mysql -u root < twister_demo.sql

# install the client for user 'user'
echo "Actual user is $USER"
sudo -u user bash << EOF
cd /home/vagrant/Twister-git_hub_branch/installer
python installer_client.py
cd /home/user/twister/bin
EOF
# start the client for 'user'
su - user -c "/home/user/twister/bin/start_client start"
