
#  _____ _           _        _      _____                  _    
# |  ___| |         | |      (_)    /  ___|                | |   
# | |__ | | ___  ___| |_ _ __ _  ___\ `--. _ __   __ _ _ __| | __
# |  __|| |/ _ \/ __| __| '__| |/ __|`--. \ '_ \ / _` | '__| |/ /
# | |___| |  __/ (__| |_| |  | | (__/\__/ / |_) | (_| | |  |   < 
# \____/|_|\___|\___|\__|_|  |_|\___\____/| .__/ \__,_|_|  |_|\_\
#                                         | |                    
#                                         |_|    
# - Description:    Main Script for the WeatherStation      
# - Author:         ElectricSpark94
# - Date:           24.04.2021      
import sys
import os
import EPaper.Control
import json
import time
from OpenWeatherMap.ImportOpenWeatherMap import OpenWeatherMap
EPD = EPaper.Control.Display()

while True:
        try:
                with open ('/home/pi/Git/PiWeatherStation/settings.json') as f:
                        settings = json.loads(f.read())      

                Weather = OpenWeatherMap(settings["OpenWeatherMap"]["Latitude"],settings["OpenWeatherMap"]["Longitude"],settings["OpenWeatherMap"]["Units"],settings["OpenWeatherMap"]["API"])
                Weather.getData()         
                EPD.Show(Weather.CurrentData,settings)
                EPD.Sleep()
                time.sleep(settings["RefreshTime"]*60)
                EPD.Init()

        except KeyboardInterrupt:    
                exit()
