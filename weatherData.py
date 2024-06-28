#!/usr/bin/python3
###############################################################################
# MIT License
#
# Copyright (c) 2024 Nuncio Bitis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
# Module defining common weather data to extract from a weather source

from weatherLocation import *

# Extracted items
city = LOCN     # City or town name
dt = 0          # Date/time of request
localtime = ""  # Local date/time from requested data
lastupdate = "" # Date/time when the weather data was last updated on the server
sunr = 0
sunrise = ""
suns = 0
sunset = ""
temp = 0.0
hpa = 0
inHg = 0
mmHg = 0
humidity = 0
uvi = 0.0
clouds = 0
speed = 0.0
direction = ""
weather = ""
weatherCode = 0
precip = 0.0
moonrise = None
moonset = None
phase = None
icon = ""
isDay = True

# For debugging, print a few parameters
def printWeatherData():
    print("City: " + city)
    print("dt: " + str(dt))
    print("localtime: " + str(localtime))
    print("lastupdate: " + str(lastupdate))
    print("Temperature: " + str(temp))
    print("Humidity: " + str(humidity))
    print("inHg: " + str(inHg))
    print("mmHg: " + str(mmHg))
    print("weather: " + weather)

###############################################################################

if __name__ == '__main__':
    print()
    print("This module is part of weather.py and is not meant to be executed alone.")
    print()
