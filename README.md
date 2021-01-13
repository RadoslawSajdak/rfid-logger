# RFID logger
## Description
Our main goal is to make system which could help us with stocktaking. We're going to do it using RFID 13.56MHz tags, and device to read it. Device will be connected with our database and app. We consider sharing our system with student research groups at our university. It will be very helpful for them because of possibility of renting tools and devices without many documents.

## Used devices
We're going to build main device on raspberry pi 4. It gives us a lot of computing power and direct connection to AGH's network with cable. We consider to use PN532 RFID module to make our project cheaper and more flexible.

## Instalation of our system
### PN532 on Raspberry Pi 4
<img src="https://botland.com.pl/64035-thickbox_default/modul-rfidnfc-pn532-1356mhz-i2cspi-karta-i-brelok.jpg" alt="PN532 Module" width="200" height="200">  
  
### Connection with SPI
This connection based on producent documentation for Raspberry Pi 4 [SITE](https://www.raspberrypi.org/documentation/usage/gpio/)
| PN532 module | Raspberry |
|:------------:|:---------:|
|     VCC      |    3.3V   |
|     GND      |    GND    |
|     MOSI     |    MOSI   |
|     MISO     |    MISO   |
|     SS       |    CE0    |
|     SCK      |    SCLK   |

**Don't forget to switch switches to 0 1 position!**

### Automatic installation
You should install raspbian with desktop from [PRODUCENT SITE](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)

After that, you have to enable SSH and add raspbery to your network. You can use this tutorial: [Tutorial](https://www.raspberrypi-spy.co.uk/2017/04/manually-setting-up-pi-wifi-using-wpa_supplicant-conf/)

First You should download our shell code (Logger_install.sh). You can send it to your raspberry with SCP:  
 - scp user/Desktop/Logger_install.sh pi@192.168.0.155:~/.   

The next step is set it's privilages with:  
 - _sudo chmod 777_ Logger_install.sh .
  
After that you should **Manually** set VNC.  
 - _sudo raspi-config_ -> _Interfacing options_ -> _VNC_ -> _Yes_

The next step is to run out script with  
 - ./Logger_install.sh

Finally you can connect to raspberry with VNC client and use our app.  
 - _python3 rfid-logger/Main.py_
## Database 

<img src="./Graphics/base.png" alt="Database structure">

## Milestones
- **20.12.2020** - Read tags and write or delete them from .txt file;
- **03.01.2020** - First version of app and database
- **17.01.2020** - Ready project. App with GUI, connected with database
