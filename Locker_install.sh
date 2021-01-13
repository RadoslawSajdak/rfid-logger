#!/bin/bash

## Update and upgrade is required for working components! ## 
sudo apt-get update
sudo apt-get upgrade -y

## All libraries use Python 3 so we need to be sure enviroment is up-to-date ## 
sudo apt-get install -y \
	python3 \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev

## It should be default-installed but we need to be sure. Don't forget to enable it with sudo raspi-config!!!! ##
sudo apt-get install realvnc-server

## We enable SPI automatically but you can set it with sudo raspi-config ##
echo "dtparam=spi=on" | sudo tee -a /boot/config.txt

## Base library for RFID scanner ##
sudo pip3 install pn532pi

## It's used mainly for debug PN532. You can check with "nfc-poll" command if your module works well (should read card) ##
sudo apt-get install -y \
	libnfc-bin \
	libnfc-examples \
	libnfc-pn53x-examples \
	git
	
## We need to clone repo with all program data and settings. Sudo is  required because we're going to replace system file ##
git clone https://gitlab.com/sajdak.radoslaw/rfid-logger.git
cd rfid-logger
git checkout MatKozyra52
sudo cp libnfc.conf /etc/nfc/libnfc.conf

##  This library is used for database. We mainly use cursor, fetch and commit functions ##
sudo pip3 install mysql-connector-python

## Just python built-in tools upgrade 
sudo pip3 install --upgrade pip setuptools virtualenv wheel

## This libraries are 
sudo apt-get install libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0

## Kivy is used for our GUI interface. You MUST install it if you want to run our app ##
sudo pip install kivy[base]

## This library has a bug. We have to replace False->True following line to run RFID reader ##
## We used two paths bc it is different sometimes and we dont know when... ##
sudo sed -i 's/self._spi.cshigh = False/self._spi.cshigh = True/g' /home/$USER/.local/lib/python3.7/site-packages/pn532pi/interfaces/pn532spi.py
sudo sed -i 's/self._spi.cshigh = False/self._spi.cshigh = True/g' /usr/local/lib/python3.7/dist-packages/pn532pi/interfaces/pn532spi.py

## You will not able to see VNC screen if you not plug-in HDMI but you want to connect with VNC
sudo echo "" | sudo tee -a /boot/config.txt
sudo echo "hdmi_force_hotplug=1" | sudo tee -a /boot/config.txt

## Reboot is required to apply all changes ##
sudo reboot

