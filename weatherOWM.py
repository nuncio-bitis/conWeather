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
# Use OpenWeatherMap API to get weather for current location
###############################################################################

import os
import json
import requests

import weatherData

from weatherLocation import *
from weatherIcons import *
from weatherConversions import *

###############################################################################

# @TODO Change this key to an OpenWeatherMap API 3.0 key
# Generic OpenWeatherMap API 2.5 key
API_KEY="85a4e3c55b73909f42c6a23ec35b7147"

UNITS="imperial" # standard (Kelvin, default), metric (Celcius), imperial (Fahrenheit)

OUT_DATA_FILE="/tmp/owm_weather.json"

# JSON object to hold server response
jsonWeather = None

###############################################################################

conditions = {
    # Group 2xx: Thunderstorm
    200: {"group": "Thunderstorm", "text": "thunderstorm with light rain"},
    201: {"group": "Thunderstorm", "text": "thunderstorm with rain"},
    202: {"group": "Thunderstorm", "text": "thunderstorm with heavy rain"},
    210: {"group": "Thunderstorm", "text": "light thunderstorm"},
    211: {"group": "Thunderstorm", "text": "thunderstorm"},
    212: {"group": "Thunderstorm", "text": "heavy thunderstorm"},
    221: {"group": "Thunderstorm", "text": "ragged thunderstorm"},
    230: {"group": "Thunderstorm", "text": "thunderstorm with light drizzle"},
    231: {"group": "Thunderstorm", "text": "thunderstorm with drizzle"},
    232: {"group": "Thunderstorm", "text": "thunderstorm with heavy drizzle"},

    # Group 3xx: Drizzle
    300: {"group": "Drizzle", "text": "light intensity drizzle"},
    301: {"group": "Drizzle", "text": "drizzle"},
    302: {"group": "Drizzle", "text": "heavy intensity drizzle"},
    310: {"group": "Drizzle", "text": "light intensity drizzle rain"},
    311: {"group": "Drizzle", "text": "drizzle rain"},
    312: {"group": "Drizzle", "text": "heavy intensity drizzle rain"},
    313: {"group": "Drizzle", "text": "shower rain and drizzle"},
    314: {"group": "Drizzle", "text": "heavy shower rain and drizzle"},
    321: {"group": "Drizzle", "text": "shower drizzle"},

    # Group 5xx: Rain
    500: {"group": "Rain", "text": "light rain"},
    501: {"group": "Rain", "text": "moderate rain"},
    502: {"group": "Rain", "text": "heavy intensity rain"},
    503: {"group": "Rain", "text": "very heavy rain"},
    504: {"group": "Rain", "text": "extreme rain"},
    511: {"group": "Rain", "text": "freezing rain"},
    520: {"group": "Rain", "text": "light intensity shower rain"},
    521: {"group": "Rain", "text": "shower rain"},
    522: {"group": "Rain", "text": "heavy intensity shower rain"},
    531: {"group": "Rain", "text": "ragged shower rain"},

    # Group 6xx: Snow
    600: {"group": "Snow", "text": "light snow"},
    601: {"group": "Snow", "text": "snow"},
    602: {"group": "Snow", "text": "heavy snow"},
    611: {"group": "Snow", "text": "sleet"},
    612: {"group": "Snow", "text": "light shower sleet"},
    613: {"group": "Snow", "text": "shower sleet"},
    615: {"group": "Snow", "text": "light rain and snow"},
    616: {"group": "Snow", "text": "rain and snow"},
    620: {"group": "Snow", "text": "light shower snow"},
    621: {"group": "Snow", "text": "shower snow"},
    622: {"group": "Snow", "text": "heavy shower snow"},

    # Group 7xx: Atmosphere
    701: {"group": "Mist", "text": "mist"},
    711: {"group": "Haze", "text": "smoke"},
    721: {"group": "Haze", "text": "haze"},
    731: {"group": "Haze", "text": "sand/dust whirls"},
    741: {"group": "Fog", "text": "fog"},
    751: {"group": "Haze", "text": "sand"},
    761: {"group": "Haze", "text": "dust"},
    762: {"group": "Haze", "text": "volcanic ash"},
    771: {"group": "Squall", "text": "squalls"},
    781: {"group": "Tornado", "text": "tornado"},

    # Group 800: Clear
    800: {"group": "Clear", "text": "clear sky"},

    # Group 80x: Clouds
    801: {"group": "Clouds", "text": "few clouds: 11-25%"},
    802: {"group": "Clouds", "text": "scattered clouds: 25-50%"},
    803: {"group": "Clouds", "text": "broken clouds: 51-84%"},
    804: {"group": "Clouds", "text": "overcast clouds: 85-100%"}
}

def displayConditions():
    print("\nWeather conditions:")
    for c in conditions:
        info = conditions[c]
        print("id=" + str(c) + " [" + info["group"] + "]", end=" ")
        print(info["text"])

def get_icon_from_code(code):
    condition = conditions[code]
    group = condition["group"]
    return get_icon(group, weatherData.isDay)

###############################################################################
# Get the current location's current weather data from the server.

def GetWeatherInfo(isRecent, DEBUG):
    """Get weather info from server"""

    # ---------------------------------
    # Get weather into JSON string

    global jsonWeather

    # Check if data is recent enough to re-use
    if isRecent:
        # Use saved data
        with open(OUT_DATA_FILE) as text_file:
            jsonWeather = json.load(text_file)
        if DEBUG: # @DEBUG
            print(80 * "-")
            print(jsonWeather)
        return

    # Build command line
    # https://api.openweathermap.org/data/3.0/onecall?lat=42.5560134&lon=-71.1092244&appid=d97c18ac18688c519a13f72a398e41e7&units=imperial&exclude=minutely,hourly,daily,alerts
    REQ_LINE = "https://api.openweathermap.org/data/3.0/onecall?" \
        + "lat=" + LAT \
        + "&lon=" + LON \
        + "&appid=" + API_KEY \
        + "&units=" + UNITS \
        + "&exclude=minutely,hourly,daily,alerts"
    
    if DEBUG: # @DEBUG
        print(80 * "-")
        print("> " + REQ_LINE)

    response = requests.get(REQ_LINE)
    jsonWeather = json.loads(response.text)

    # Write JSON response to file to format it for reading
    with open(OUT_DATA_FILE + ".raw", "w") as text_file:
        text_file.write(response.text)
    os.system("jq < " + OUT_DATA_FILE + ".raw > " + OUT_DATA_FILE)
    # Remove the unformatted output file
    os.system("rm -f " + OUT_DATA_FILE + ".raw")

    if DEBUG: # @DEBUG
        print(80 * "-")
        print(jsonWeather)

###############################################################################
# Extract current weather data from the received data file.

def ExtractWeatherData():
    # ---------------------------------
    # Parse data for weather items

    # Date/time
    weatherData.dt = jsonWeather["current"]["dt"]
    weatherData.localtime = seconds_to_local(weatherData.dt)
    weatherData.lastupdate = weatherData.localtime
    # Sunrise & sunset
    weatherData.sunr = jsonWeather["current"]["sunrise"]
    weatherData.sunrise = seconds_to_time(weatherData.sunr)
    weatherData.suns = jsonWeather["current"]["sunset"]
    weatherData.sunset = seconds_to_time(weatherData.suns)
    # Temperature
    weatherData.temp = jsonWeather["current"]["temp"]
    # Pressure
    weatherData.hpa = jsonWeather["current"]["pressure"]
    weatherData.inHg = hPa_to_inHg(weatherData.hpa)
    weatherData.mmHg = inHg_to_mmHg(weatherData.inHg)
    # Humidity
    weatherData.humidity = jsonWeather["current"]["humidity"]
    # Ultraviolet index
    weatherData.uvi = jsonWeather["current"]["uvi"]
    # Cloud cover (percentage)
    weatherData.clouds = jsonWeather["current"]["clouds"]
    # Wind speed and direction
    weatherData.speed = jsonWeather["current"]["wind_speed"]
    weatherData.dir = jsonWeather["current"]["wind_deg"]
    if (weatherData.direction is None):
        weatherData.direction = ""
    else:
        weatherData.direction = degToCompass(weatherData.dir)
    # Current conditions
    weatherData.weather = jsonWeather["current"]["weather"][0]["main"]
    weatherData.weatherCode = jsonWeather["current"]["weather"][0]["id"]
    # Precipitation - Not reliable. Not always in the data.
    # weatherData.precipitation = jsonWeather["current"]["rain"]["1h"]
    # if (weatherData.precipitation is None):
    #     weatherData.precip = "None"
    weatherData.precip = None

    # icon = get_icon(weather)
    icon = get_icon_from_code(weatherData.weatherCode)

###############################################################################

if __name__ == '__main__':
    print()
    print("This module is part of weather.py and is not meant to be executed alone.")
    print()

