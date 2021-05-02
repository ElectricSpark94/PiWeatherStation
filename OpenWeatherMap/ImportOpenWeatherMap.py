import requests
import json
import logging
from datetime import datetime
from pytz import timezone

#------------------------------------------------------------------------------------------------------------------
# OpenWeatherMap 
#------------------------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)


class OpenWeatherMap():
    def __init__(self,lat,lon,units,api_key):
        self.CurrentData=""
        self.lat= lat
        self.lon= lon
        self.units= units
        self.api_key= api_key
        self.url  = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=%s" % (self.lat, self.lon,self.api_key,self.units)

    def getData(self):
        try:
            response = requests.get(self.url)
            self.CurrentData = json.loads(response.text)
            logging.info("Successfully received data from OpenWeatherMap "+ datetime.now(timezone("Europe/Berlin")).strftime("%Y-%m-%d %H:%M"))
        
        except OSError as err:
            logging.error("OS error: {0}".format(err))
    
    def WriteJson(self):
        with open("WeatherData.json","w") as fout:
            fout.write(json.dumps(self.CurrentData,indent=4))




