import requests
import json
import logging
from datetime import datetime
from pytz import timezone

#------------------------------------------------------------------------------------------------------------------
# OpenWeatherMap Setup
#------------------------------------------------------------------------------------------------------------------
api_key = "7e45a2bf8a32e9bbe1c85ea46d1dc89f"
lat = "49.2946"
lon = "8.6964"
urlCurrent = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
logging.basicConfig(level=logging.INFO)
# Global Variable

class OpenWeatherMap():
    def __init__(self,lat,lon,api_key):
        self.CurrentData=""
        self.CurrentDay=""
        self.CurrentDate=""
        self.lat= lat
        self.lon= lon
        self.api_key= api_key
        self.url  = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, self.api_key)

    def getData(self):
        try:
            response = requests.get(urlCurrent)
            self.CurrentData = json.loads(response.text)
            logging.info("Successfully received data from OpenWeatherMap "+ datetime.now(timezone("Europe/Berlin")).strftime("%Y-%m-%d %H:%M"))
            self.CurrentDay=datetime.utcfromtimestamp(self.CurrentData["current"]["dt"]).strftime('%A')
            self.Translate(self.CurrentDay)
            self.CurrentDate=self.CurrentDay+ ", "+datetime.utcfromtimestamp(self.CurrentData["current"]["dt"]).strftime('%d.%m.%Y')
            self.WriteJson()
        
        except OSError as err:
            logging.error("OS error: {0}".format(err))

    def Translate(self,toTranslate):
        if toTranslate == "Monday":
            self.day= "Montag"
        elif toTranslate =="Tuesday":
            self.day = "Dienstag"
        elif toTranslate == "Wednesday":
            self.day = "Mittwoch"
        elif toTranslate == "Thursday":
            self.day = "Donnerstag"
        elif toTranslate == "Friday":
            self.day = "Freitag"
        elif toTranslate == "Saturday":
            self.day = "Samstag"
        elif toTranslate == "Sunday":
            self.day = "Sonntag"
        else:
            logging.info("No translation available")
    
    def WriteJson(self):
        with open("WeatherData.json","w") as fout:
            fout.write(json.dumps(self.CurrentData,indent=4))


Current = OpenWeatherMap("49.2946","8.6964","7e45a2bf8a32e9bbe1c85ea46d1dc89f")
Current.getData()


