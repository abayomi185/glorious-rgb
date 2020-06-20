from flask import Flask, escape, request, redirect, render_template
from datetime import datetime
import pigpio
import time
import json
import logging

app = Flask(__name__)

# Disable logs except errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

PWM_RED=12
PWM_GREEN=19
PWM_BLUE=13

pi = pigpio.pi()

gloriousRGBHex = "#FFFFFF"

hex_dict = {"color": ""}

########################################### Functions ########################################### 

def saveToJSON():
    hex_dict["color"] = gloriousRGBHex
    with open('save.json', 'w') as jsonfile:
        json.dump(hex_dict, jsonfile)

def retrieveFromJSON():
    global gloriousRGBHex
    with open('save.json') as json_file:
        hex_dict = json.load(json_file)
    gloriousRGBHex = hex_dict["color"]

def convertHexToRGB(hexValue):
    hexValue = hexValue.lstrip('#')
    #lv = len(hexvalue)
    #return tuple(int(hexvalue[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return tuple(int(hexValue[i:i+2], 16) for i in (0, 2, 4))

def enableGloriousRGB(colour):
    pi.set_PWM_dutycycle(PWM_RED, (colour[0]))
    pi.set_PWM_dutycycle(PWM_GREEN, (colour[1]))
    pi.set_PWM_dutycycle(PWM_BLUE, (colour[2]))

######################################### End of Functions #########################################

# Functiom call
# Retrieves color hex from json file at launch
retrieveFromJSON()

########################################### Flask Section ########################################### 
@app.route('/', methods=['POST', 'GET'])
def home():

    # This is here because I learned python is a bit of a bitch
    # Python wouldn't know that gloriousRGBHex is a global variable unless this is here
    global gloriousRGBHex

    RGBHex = gloriousRGBHex

    if request.method == 'POST':
        gloriousRGBHex = request.form['hexValue']
        saveToJSON()
        rgbValue = convertHexToRGB(gloriousRGBHex)
        enableGloriousRGB(rgbValue)
    else:
        pass
    return render_template('index.html', RGBHex=RGBHex)
    # The first RGBHex is the value I'm using in the html and the second is the value declared above

if __name__ == '__main__':
    app.run(host= '10.0.1.11', port=5050)
    #app.run(port=5001) - old line that is integrated to line above
    #Debug basically allows calling the python script to run as flask
    #It also allows webpage to be updated without ending and starting script

#export FLASK_APP=firstflask.py

####################################### End of Flask Section ######################################