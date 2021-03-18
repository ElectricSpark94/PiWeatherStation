import sys
import os
import json
from flask import Flask, redirect, url_for, render_template , request
import logging


app= Flask(__name__,static_folder='/')

with open("./templates/settings.json") as f:
    data = json.load(f)


@app.route("/",methods=["POST","GET"])
def default():
    if request.method== "POST": 
        data["Settings"]["City"]= request.form["city"]    
        data["Settings"]["API"]= request.form["api"]
        data["Settings"]["Latitude"]= request.form["Latitude"]
        data["Settings"]["Longitude"]= request.form["Longitude"]
        #with open("./settings.json","w") as fout:
        #    fout.write(json.dumps(data,indent=4))
        return render_template("MainPage.html",API =data["Settings"]["API"],Latitude=data["Settings"]["Latitude"],Longitude=data["Settings"]["Longitude"],Unit=data["Settings"]["Unit"],City=data["Settings"]["City"] )
    else:
        return render_template("MainPage.html",API =data["Settings"]["API"],Latitude=data["Settings"]["Latitude"],Longitude=data["Settings"]["Longitude"],Unit=data["Settings"]["Unit"],City=data["Settings"]["City"] )

@app.route("/<default>")
def user(default):
    return render_template("Defaultpage.html")
    

if __name__ == "__main__":
    app.run(debug="True" )