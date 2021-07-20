#  _____ _           _        _      _____                  _    
# |  ___| |         | |      (_)    /  ___|                | |   
# | |__ | | ___  ___| |_ _ __ _  ___\ `--. _ __   __ _ _ __| | __
# |  __|| |/ _ \/ __| __| '__| |/ __|`--. \ '_ \ / _` | '__| |/ /
# | |___| |  __/ (__| |_| |  | | (__/\__/ / |_) | (_| | |  |   < 
# \____/|_|\___|\___|\__|_|  |_|\___\____/| .__/ \__,_|_|  |_|\_\
#                                         | |                    
#                                         |_|    
# - Description:    This module create the image for the epd_waveshare 7.5" display      
# - Author:         ElectricSpark94
# - Date:           24.04.2021           
#------------------------------------------------------------
#   SYS / OS MODULS 
#------------------------------------------------------------
import sys
import os

#------------------------------------------------------------
#   Directory  
#------------------------------------------------------------
DirectoryEPaper = os.getcwd()+os.path.join("/EPaper")
sys.path.append(os.getcwd()+os.path.join("/EPaper"))
sys.path.append("/home/pi/Git/PiWeatherStation/EPaper")

DirectoryEPaper = "/home/pi/Git/PiWeatherStation/EPaper/"


DirectoryCommonIcon = os.getcwd()+os.path.join("/EPaper/Icon/Common/")
DirectoryWeatherIcon = os.getcwd()+os.path.join("/EPaper/Icon/Weather/")

DirectoryCommonIcon = "/home/pi/Git/PiWeatherStation/EPaper/Icon/Common/"
DirectoryWeatherIcon = "/home/pi/Git/PiWeatherStation/EPaper/Icon/Weather/"

#------------------------------------------------------------
#   OTHER MODULS 
#------------------------------------------------------------

from datetime import datetime
from pytz import timezone
import json
import logging
import epd7in5b_HD
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import locale
import pytz
import tzlocal

#------------------------------------------------------------
#   DEBUG LEVEL  
#------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG)


class Display:
    def __init__(self):
        #Font
        self.font100 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 100)
        self.font90 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 90)
        self.font70 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 70)
        self.font64 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 64)
        self.font56 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 56)
        self.font46 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 46)
        self.font40 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 40)
        self.font32 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 32)
        self.font26 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 26)
        self.font24 = ImageFont.truetype(DirectoryEPaper + os.path.join('/Dense-Regular.ttc'), 24)  
        
        self.epd = epd7in5b_HD.EPD()
        logging.info("init and Clear")
        self.epd.init()
        self.epd.Clear()
        
    
    def Show(self,data,settings):
        try:
            # Create Image
            logging.info("Drawing on the image...")
            Bimage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
            Rimage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
            draw_RImage = ImageDraw.Draw(Rimage)
            draw_BImage = ImageDraw.Draw(Bimage)

            #City
            draw_RImage.text((86, 21), settings["City"], font = self.font70, fill = 0)
            
            #CurrentTemp
            width, height = draw_BImage.textsize(settings["City"] , font = self.font70)
            XPosition = 86+width+20
            YPosition = 21
            draw_BImage.text((XPosition ,YPosition), "{}".format(round(float(data["current"]["temp"]))), font = self.font70, fill = 0)
            width, height = draw_BImage.textsize("{}".format(round(float(data["current"]["temp"]))), font = self.font70)
            draw_BImage.text((width+XPosition+1, 24), settings["OpenWeatherMap"]["UnitsFormat"], font = self.font40, fill = 0)

            #Placeholder:
            Position= (30,30)
            Size = (50,50)
            Image_black = Image.open(DirectoryCommonIcon + os.path.join('placeholder_black.bmp'))
            Image_red = Image.open(DirectoryCommonIcon + os.path.join('placeholder_red.bmp')) 
            Image_black.thumbnail(Size)
            Image_red.thumbnail(Size)
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)
            
            #CurrentWeatherIcon:
            Position= (45,125)
            Size = (250,250)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["current"]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["current"]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)

            #Today/Temp. min/max:
            Position= (340,135)
            Size = (40,40)
            Image_black = Image.open(DirectoryCommonIcon + os.path.join('temperature_black.bmp'))
            Image_red = Image.open(DirectoryCommonIcon + os.path.join('temperature_red.bmp')) 
            Image_black.thumbnail(Size)
            Image_red.thumbnail(Size)
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)

            #Calc. Text width for Position:
            width, height =  draw_BImage.textsize("{}/{}".format(round(float(data["daily"][0]["temp"]["min"])),round(float(data["daily"][0]["temp"]["max"]))) ,font = self.font40)
            if settings["OpenWeatherMap"]["Units"]== "imperial":
                width, height =  draw_BImage.textsize("{}".format( "{}/{}".format(round(float(data["daily"][0]["temp"]["min"])),round(float(data["daily"][0]["temp"]["max"])))) ,font = self.font40)
            else:
                width, height =  draw_BImage.textsize("{}/{}".format(round(float(data["daily"][0]["temp"]["min"])),round(float(data["daily"][0]["temp"]["max"]))) ,font = self.font40)

            XPosition = 410+width
            draw_BImage.text((XPosition-width, 135), "{}/{}".format(round(float(data["daily"][0]["temp"]["min"])),round(float(data["daily"][0]["temp"]["max"]))),font = self.font40, fill = 0)
            draw_BImage.text((XPosition+2, 135),settings["OpenWeatherMap"]["UnitsFormat"],font = self.font26, fill = 0)

            #Today/Humidity:
            Position= (340,185)
            Size = (40,40)
            Image_black = Image.open(DirectoryCommonIcon + os.path.join('humidity_black.bmp'))
            Image_red = Image.open(DirectoryCommonIcon + os.path.join('humidity_red.bmp')) 
            Image_black.thumbnail(Size)
            Image_red.thumbnail(Size)
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)

            width, height = draw_BImage.textsize("{}".format(data["current"]["humidity"]),font = self.font40)  
            draw_BImage.text((XPosition-width, 185), "{}".format(data["current"]["humidity"]) ,font = self.font40, fill = 0)
            draw_BImage.text((XPosition+3, 185),"%",font = self.font26, fill = 0)

            #Today/Pressure:
            Position= (340,235)
            Size = (40,40)
            Image_black = Image.open(DirectoryCommonIcon + os.path.join('barometer_black.bmp'))
            Image_red = Image.open(DirectoryCommonIcon + os.path.join('barometer_red.bmp')) 
            Image_black.thumbnail(Size)
            Image_red.thumbnail(Size)
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)

            width, height = draw_BImage.textsize("{}".format(data["current"]["pressure"]) ,font = self.font40) 
            draw_BImage.text((XPosition-width, 235), "{}".format(data["current"]["pressure"]),font = self.font40, fill = 0)
            draw_BImage.text((XPosition+3, 235),"mbar",font = self.font26, fill = 0)

            #Today/Rain:
            Position= (340,285)
            Size = (40,40)
            Image_black = Image.open(DirectoryCommonIcon + os.path.join('umbrella_black.bmp'))
            Image_red = Image.open(DirectoryCommonIcon + os.path.join('umbrella_red.bmp')) 
            Image_black.thumbnail(Size)
            Image_red.thumbnail(Size)
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)

            width, height = draw_BImage.textsize("{}".format(round(data["daily"][0]["pop"]*100)),font = self.font40) 
            draw_BImage.text((XPosition-width, 285), "{}".format(round(float(data["daily"][0]["pop"]*100))),font = self.font40, fill = 0)
            draw_BImage.text((XPosition+3, 285),"%",font = self.font26, fill = 0)


            #Today/Wind:
            Position= (340,335)
            Size = (40,40)
            Image_black = Image.open(DirectoryCommonIcon + os.path.join('windsock_black.bmp'))
            Image_red = Image.open(DirectoryCommonIcon + os.path.join('windsock_red.bmp')) 
            Image_black.thumbnail(Size)
            Image_red.thumbnail(Size)
            Bimage.paste(Image_black, Position)
            Rimage.paste(Image_red, Position)

            width, height = draw_BImage.textsize("{}".format(data["current"]["wind_speed"]),font = self.font40) 
            draw_BImage.text((XPosition-width, 335), "{}".format(data["current"]["wind_speed"]),font = self.font40, fill = 0)
            draw_BImage.text((XPosition+3, 335),"km/h",font = self.font26, fill = 0)

            #Date
            draw_BImage.text((40, 400), datetime.utcfromtimestamp(data["current"]["dt"]).strftime('%A') +", " +datetime.utcfromtimestamp(data["current"]["dt"]).strftime(settings["OpenWeatherMap"]["DateFormat1"]), font = self.font46, fill = 0)

            #Diagram
            #Setting:
            YPosition=560
            CircleRadius=5
            draw_BImage.line((40,YPosition, 488,YPosition), fill=0)
            if settings["OpenWeatherMap"]["Units"]== "imperial":
                Factor = 25
            else:
                Factor = 100

            #First Value
            XValue1=60
            YValue1= float(data["hourly"][1]["temp"])*Factor/50
            draw_BImage.ellipse(([(XValue1-CircleRadius,YPosition-CircleRadius),(XValue1+CircleRadius,YPosition+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize(datetime.utcfromtimestamp(data["hourly"][1]["dt"]).strftime('%H:%M'),font=self.font26)
            draw_BImage.text((XValue1-width/2,YPosition+10),datetime.utcfromtimestamp(data["hourly"][1]["dt"]).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()).strftime('%H:%M'),font=self.font26, fill = 0)
            draw_RImage.ellipse(([(XValue1-CircleRadius,YPosition-YValue1-CircleRadius),(XValue1+CircleRadius,YPosition-YValue1+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize("{}".format(round(float(data["hourly"][1]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"],font=self.font24)
            draw_BImage.text((XValue1-width/2, YPosition-YValue1-30), "{}".format(round(float(data["hourly"][1]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"], font = self.font24, fill = 0)
            #Graphic
            GraphicX= round(XValue1-40/2)
            GraphicY = round(YPosition-YValue1-75)
            Position = (GraphicX,GraphicY)
            Size = (40,40)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["hourly"][1]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["hourly"][1]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            #Second Value
            XValue2=196
            YValue2= float(data["hourly"][3]["temp"])*Factor/50
            draw_BImage.ellipse(([(XValue2-CircleRadius,YPosition-CircleRadius),(XValue2+CircleRadius,YPosition+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize(datetime.utcfromtimestamp(data["hourly"][3]["dt"]).strftime('%H:%M'),font=self.font26)
            draw_BImage.text((XValue2-width/2,YPosition+10),datetime.utcfromtimestamp(data["hourly"][3]["dt"]).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()).strftime('%H:%M'),font=self.font26, fill = 0)
            draw_RImage.ellipse(([(XValue2-CircleRadius,YPosition-YValue2-CircleRadius),(XValue2+CircleRadius,YPosition-YValue2+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize("{}".format(round(float(data["hourly"][3]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"],font=self.font24)
            draw_BImage.text((XValue2-width/2, YPosition-YValue2-30), "{}".format(round(float(data["hourly"][3]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"], font = self.font24, fill = 0)
            #Graphic
            GraphicX= round(XValue2-40/2)
            GraphicY = round(YPosition-YValue2-75)
            Position = (GraphicX,GraphicY)
            Size = (40,40)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["hourly"][3]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["hourly"][3]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            draw_RImage.line((XValue1,YPosition-YValue1, XValue2,YPosition-YValue2), fill=0)

            #Thrid Value
            XValue3=332
            YValue3= float(data["hourly"][5]["temp"])*Factor/50
            draw_BImage.ellipse(([(XValue3-CircleRadius,YPosition-CircleRadius),(XValue3+CircleRadius,YPosition+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize(datetime.utcfromtimestamp(data["hourly"][5]["dt"]).strftime('%H:%M'),font=self.font26)
            draw_BImage.text((XValue3-width/2,YPosition+10),datetime.utcfromtimestamp(data["hourly"][5]["dt"]).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()).strftime('%H:%M'),font=self.font26, fill = 0)
            draw_RImage.ellipse(([(XValue3-CircleRadius,YPosition-YValue3-CircleRadius),(XValue3+CircleRadius,YPosition-YValue3+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize("{}".format(round(float(data["hourly"][5]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"],font=self.font24)
            draw_BImage.text((XValue3-width/2, YPosition-YValue3-30), "{}".format(round(float(data["hourly"][5]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"], font = self.font24, fill = 0)
            #Graphic
            GraphicX= round(XValue3-40/2)
            GraphicY = round(YPosition-YValue3-75)
            Position = (GraphicX,GraphicY)
            Size = (40,40)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["hourly"][5]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["hourly"][5]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            draw_RImage.line((XValue2,YPosition-YValue2, XValue3,YPosition-YValue3), fill=0)

            #Fourth Value
            XValue4=468
            YValue4= float(data["hourly"][7]["temp"])*Factor/50
            draw_BImage.ellipse(([(XValue4-CircleRadius,YPosition-CircleRadius),(XValue4+CircleRadius,YPosition+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize(datetime.utcfromtimestamp(data["hourly"][7]["dt"]).strftime('%H:%M'),font=self.font26)
            draw_BImage.text((XValue4-width/2,YPosition+10),datetime.utcfromtimestamp(data["hourly"][7]["dt"]).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()).strftime('%H:%M'),font=self.font26, fill = 0)
            draw_RImage.ellipse(([(XValue4-CircleRadius,YPosition-YValue4-CircleRadius),(XValue4+CircleRadius,YPosition-YValue4+CircleRadius)]),fill=0)
            width, height = draw_BImage.textsize("{}".format(round(float(data["hourly"][7]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"],font=self.font24)
            draw_BImage.text((XValue4-width/2, YPosition-YValue4-30), "{}".format(round(float(data["hourly"][7]["temp"])))+settings["OpenWeatherMap"]["UnitsFormat"], font = self.font24, fill = 0)

            #Graphic
            GraphicX= round(XValue4-40/2)
            GraphicY = round(YPosition-YValue4-75)
            Position = (GraphicX,GraphicY)
            Size = (40,40)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["hourly"][5]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["hourly"][5]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            draw_RImage.line((XValue3,YPosition-YValue3, XValue4,YPosition-YValue4), fill=0)


        
            #Forecast +1 day:
            Day= datetime.utcfromtimestamp(data["daily"][1]["dt"]).strftime('%A')
            Date = datetime.utcfromtimestamp(data["daily"][1]["dt"]).strftime(settings["OpenWeatherMap"]["DateFormat2"])
            Temp_MinMax = "{}".format(round(float(data["daily"][1]["temp"]["min"]))) +"/"+"{}".format(round(float(data["daily"][1]["temp"]["max"])))+settings["OpenWeatherMap"]["UnitsFormat"]
            Pop =  "{}%".format(round(float(data["daily"][1]["pop"]*100)))

            Position = (61,700)
            Size = (80,80)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["daily"][1]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["daily"][1]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            width, height = draw_BImage.textsize( datetime.utcfromtimestamp(data["daily"][1]["dt"]).strftime('%A')+ ",", font=self.font32)
            draw_BImage.multiline_text((61+40-(width/2),627), Day +",\n" + Date + "\n \n \n \n" + Temp_MinMax + "\n" + Pop, font= self.font32, align ="center",fill=(0))

            #Forecast +2 day:
            Day= datetime.utcfromtimestamp(data["daily"][2]["dt"]).strftime('%A')
            Date = datetime.utcfromtimestamp(data["daily"][2]["dt"]).strftime(settings["OpenWeatherMap"]["DateFormat2"])
            Temp_MinMax = "{}".format(round(float(data["daily"][2]["temp"]["min"]))) +"/"+"{}".format(round(float(data["daily"][2]["temp"]["max"])))+settings["OpenWeatherMap"]["UnitsFormat"]
            Pop =  "{}%".format(round(float(data["daily"][2]["pop"]*100)))

            Position= (224,700)
            Size = (80,80)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["daily"][2]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["daily"][2]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            width, height = draw_BImage.textsize( datetime.utcfromtimestamp(data["daily"][2]["dt"]).strftime('%A')+ ",", font=self.font32)
            draw_BImage.multiline_text((224+40-(width/2),627), Day +",\n" + Date + "\n \n \n \n" + Temp_MinMax + "\n" + Pop, font= self.font32, align ="center",fill=(0))

            #Forecast +3 day:
            Day= datetime.utcfromtimestamp(data["daily"][3]["dt"]).strftime('%A')
            Date = datetime.utcfromtimestamp(data["daily"][3]["dt"]).strftime(settings["OpenWeatherMap"]["DateFormat2"])
            Temp_MinMax = "{}".format(round(float(data["daily"][3]["temp"]["min"]))) +"/"+"{}".format(round(float(data["daily"][3]["temp"]["max"])))+settings["OpenWeatherMap"]["UnitsFormat"]
            Pop =  "{}%".format(round(float(data["daily"][3]["pop"]*100)))

            Position= (388,700)
            Size = (80,80)
            Image_red = Image.open(DirectoryWeatherIcon + os.path.join("{}_red.bmp".format(data["daily"][3]["weather"][0]["icon"]))) 
            Image_black = Image.open(DirectoryWeatherIcon + os.path.join("{}_black.bmp".format(data["daily"][3]["weather"][0]["icon"])))
            Image_red.thumbnail(Size )
            Image_black.thumbnail(Size )
            Rimage.paste(Image_red, Position)
            Bimage.paste(Image_black, Position)

            width, height = draw_BImage.textsize( datetime.utcfromtimestamp(data["daily"][3]["dt"]).strftime('%A')+ ",", font=self.font32)
            draw_BImage.multiline_text((388+40-(width/2),627), Day +",\n" + Date + "\n \n \n \n" + Temp_MinMax + "\n" + Pop, font= self.font32, align ="center",fill=(0))
            

            self.epd.display(self.epd.getbuffer(Bimage),self.epd.getbuffer(Rimage))
        
        except IOError as e:
            logging.info(e)
                
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd7in5b_HD.epdconfig.module_exit()
            exit()
    
    def Sleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()

    def Clear(self):
        self.epd.Clear()
        logging.info("Clear Screen...")
    
    def Init(self):
        self.epd.init()
        logging.info("Init Screen...")

