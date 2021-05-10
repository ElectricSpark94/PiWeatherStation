# PiWeatherStation

## Installation 

1. Install Raspberry Pi OS Lite on an SD card. A short description can be found on the Raspberry Pi homepage [[click here](https://www.raspberrypi.org/software/ "Raspberry Pi OS")]

2. Enable SSH on a headless Raspberry Pi [[click here](https://www.raspberrypi.org/documentation/remote-access/ssh/ "click here")]

3. Connect with SSH and enable the SPI interface via raspi-config
```python
sudo raspi-config
```
After activation you should reboot the Pi.
```python
sudo reboot
```
### Install BCM2835 libraries
```python
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz 
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
```

### Install WiringPi libraries
```python
sudo apt-get install wiringpi
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
```

### Install Python3 libraries
```python
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
sudo apt install git 
```
### Download demo codes from Waveshare
Download actual GIT repository
```python
sudo git clone https://github.com/waveshare/e-Paper
```
Run the Demo code
```python
cd ~/e-Paper/RaspberryPi_JetsonNano/python/examples/
sudo python3 epd_7in5b_V2_test.py
```
The demo code should work to operate the weather station

### Install Pi#Weatherstation
Install libraries
```python
cd
sudo pip3 install requests
sudo pip3 install pytz
sudo pip3 install tzlocal
sudo pip3 install Pillow
sudo pip3 install numpy
sudo pip3 install logging

```
Download actual GIT repository
```python
sudo mkdir Git
cd Git
sudo git clone https://github.com/ElectricSpark94/PiWeatherStation.git
cd PiWeatherStation
```
Run the Main.py
```python
sudo python3 Main.py
```
---
# Settings
In the Settings.json the [Openweathermap](https://openweathermap.org/appid "Openweathermap") API-Key must be added. Furthermore, the city, the geographical location and the unit must be set.
e.g.


|  Setting  | Description |
| ------------- | ------------- |
| City   | Name of the city e.g. "San Francisco"  |
| RefreshTime  | Time of display refresh in minutes e.g. "10"  |
|API| API-Key must be added|
|Latitude|e.g. "37.7739"|
|Longitude|e.g. "-122.4312"|
|Units|"metric"for °C, "imperial" for F or "standard" for Kelvin|
|UnitsFormat| Unit format e.g. "°C" or "F"|
|DateFormat1| Date format e.g. "%m/%d/%Y"|
|DateFormat2|Date format e.g. "%m/%d"|

