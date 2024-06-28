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
# Use WeatherAPI to get weather for current location
###############################################################################

import os
import json
import requests

import weatherData

from weatherLocation import *
from weatherIcons import *
from weatherConversions import *

###############################################################################

# @TODO WeatherAPI API Token
API_KEY=None

# Query code, either ZIP
#QUERY="&q=" + ZIP
# or GPS coords
QUERY="&q=" + LAT + "," + LON

OUT_DATA_FILE="/tmp/wapi_weather.json"
OUT_ASTRO_FILE="/tmp/wapi_astro.json"

# JSON objects to hold server responses
jsonWeather = None
jsonAstro = None

###############################################################################

# code: group,day,night,icon
conditions = {
    1000: {"group": "Clear", "day": "Sunny", "night": "Clear", "icon": 113},

    1003: {"group": "Clouds", "day": "Partly cloudy", "night": "Partly cloudy", "icon": 116},
    1006: {"group": "Clouds", "day": "Cloudy", "night": "Cloudy", "icon": 119},
    1009: {"group": "Clouds", "day": "Overcast", "night": "Overcast", "icon": 122},

    1030: {"group": "Mist", "day": "Mist", "night": "Mist", "icon": 143},

    1135: {"group": "Fog", "day": "Fog", "night": "Fog", "icon": 248},
    1147: {"group": "Fog", "day": "Freezing fog", "night": "Freezing fog", "icon": 260},

    1063: {"group": "Rain", "day": "Patchy rain possible", "night": "Patchy rain possible", "icon": 176},
    1150: {"group": "Rain", "day": "Patchy light drizzle", "night": "Patchy light drizzle", "icon": 263},
    1153: {"group": "Rain", "day": "Light drizzle", "night": "Light drizzle", "icon": 266},
    1168: {"group": "Rain", "day": "Freezing drizzle", "night": "Freezing drizzle", "icon": 281},
    1171: {"group": "Rain", "day": "Heavy freezing drizzle", "night": "Heavy freezing drizzle", "icon": 284},
    1180: {"group": "Rain", "day": "Patchy light rain", "night": "Patchy light rain", "icon": 293},
    1183: {"group": "Rain", "day": "Light rain", "night": "Light rain", "icon": 296},
    1186: {"group": "Rain", "day": "Moderate rain at times", "night": "Moderate rain at times", "icon": 299},
    1189: {"group": "Rain", "day": "Moderate rain", "night": "Moderate rain", "icon": 302},
    1192: {"group": "Rain", "day": "Heavy rain at times", "night": "Heavy rain at times", "icon": 305},
    1195: {"group": "Rain", "day": "Heavy rain", "night": "Heavy rain", "icon": 308},
    1198: {"group": "Rain", "day": "Light freezing rain", "night": "Light freezing rain", "icon": 311},
    1201: {"group": "Rain", "day": "Moderate or heavy freezing rain", "night": "Moderate or heavy freezing rain", "icon": 314},
    1240: {"group": "Rain", "day": "Light rain shower", "night": "Light rain shower", "icon": 353},
    1243: {"group": "Rain", "day": "Moderate or heavy rain shower", "night": "Moderate or heavy rain shower", "icon": 356},
    1246: {"group": "Rain", "day": "Torrential rain shower", "night": "Torrential rain shower", "icon": 359},

    1066: {"group": "Snow", "day": "Patchy snow possible", "night": "Patchy snow possible", "icon": 179},
    1114: {"group": "Snow", "day": "Blowing snow", "night": "Blowing snow", "icon": 227},
    1117: {"group": "Snow", "day": "Blizzard", "night": "Blizzard", "icon": 230},
    1210: {"group": "Snow", "day": "Patchy light snow", "night": "Patchy light snow", "icon": 323},
    1213: {"group": "Snow", "day": "Light snow", "night": "Light snow", "icon": 326},
    1216: {"group": "Snow", "day": "Patchy moderate snow", "night": "Patchy moderate snow", "icon": 329},
    1219: {"group": "Snow", "day": "Moderate snow", "night": "Moderate snow", "icon": 332},
    1222: {"group": "Snow", "day": "Patchy heavy snow", "night": "Patchy heavy snow", "icon": 335},
    1225: {"group": "Snow", "day": "Heavy snow", "night": "Heavy snow", "icon": 338},
    1255: {"group": "Snow", "day": "Light snow showers", "night": "Light snow showers", "icon": 368},
    1258: {"group": "Snow", "day": "Moderate or heavy snow showers", "night": "Moderate or heavy snow showers", "icon": 371},

    1069: {"group": "Snow", "day": "Patchy sleet possible", "night": "Patchy sleet possible", "icon": 182},
    1072: {"group": "Snow", "day": "Patchy freezing drizzle possible", "night": "Patchy freezing drizzle possible", "icon": 185},
    1204: {"group": "Snow", "day": "Light sleet", "night": "Light sleet", "icon": 317},
    1207: {"group": "Snow", "day": "Moderate or heavy sleet", "night": "Moderate or heavy sleet", "icon": 320},
    1237: {"group": "Snow", "day": "Ice pellets", "night": "Ice pellets", "icon": 350},
    1249: {"group": "Snow", "day": "Light sleet showers", "night": "Light sleet showers", "icon": 362},
    1252: {"group": "Snow", "day": "Moderate or heavy sleet showers", "night": "Moderate or heavy sleet showers", "icon": 365},
    1261: {"group": "Snow", "day": "Light showers of ice pellets", "night": "Light showers of ice pellets", "icon": 374},
    1264: {"group": "Snow", "day": "Moderate or heavy showers of ice pellets", "night": "Moderate or heavy showers of ice pellets", "icon": 377},

    1087: {"group": "Thunderstorm", "day": "Thundery outbreaks possible", "night": "Thundery outbreaks possible", "icon": 200},
    1273: {"group": "Thunderstorm", "day": "Patchy light rain with thunder", "night": "Patchy light rain with thunder", "icon": 386},
    1276: {"group": "Thunderstorm", "day": "Moderate or heavy rain with thunder", "night": "Moderate or heavy rain with thunder", "icon": 389},
    1279: {"group": "Thunderstorm", "day": "Patchy light snow with thunder", "night": "Patchy light snow with thunder", "icon": 392},
    1282: {"group": "Thunderstorm", "day": "Moderate or heavy snow with thunder", "night": "Moderate or heavy snow with thunder", "icon": 395},
}

def displayConditions():
    print("\nWeather conditions:")
    for c in conditions:
        info = conditions[c]
        print("id=" + str(c) + " [" + info["group"] + "]", end=" ")
        if info["day"] == info["night"]:
            print(info["day"])
        else:
            print("Day:(" + info["day"] + ") Night:(" + info["night"] + ")")

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
        GetAstroInfo(isRecent, DEBUG)
        return

    # Build command line
    # https://api.weatherapi.com/v1/current.json?key=[API_KEY]&q=[ZIP]&aqi=yes
    REQ_LINE = "https://api.weatherapi.com/v1/current.json?" \
        + "key=" + API_KEY \
        + QUERY + "&aqi=yes"

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

    # This server has another API call to get more data
    GetAstroInfo(isRecent, DEBUG)


###############################################################################
# Get the current location's astronomical data from the server.

def GetAstroInfo(isRecent, DEBUG):
    """Get astronomy info from server"""

    # ---------------------------------
    # Get data into JSON string

    global jsonAstro

    # Check if data is recent enough to re-use
    if isRecent:
        # Use saved data
        with open(OUT_ASTRO_FILE) as text_file:
            jsonAstro = json.load(text_file)
        if DEBUG: # @DEBUG
            print(80 * "-")
            print(jsonAstro)
        return

    # Build command line
    # https://api.weatherapi.com/v1/astronomy.json?key=[API_KEY]&q=[ZIP]
    REQ_LINE = "https://api.weatherapi.com/v1/astronomy.json?" \
        + "key=" + API_KEY \
        + "&q=" + ZIP

    # @DEBUG
    if (DEBUG == 1):
        print(80 * "-")
        print("> " + REQ_LINE)

    response = requests.get(REQ_LINE)
    jsonAstro = json.loads(response.text)

    # Write JSON response to file to format it for reading
    with open(OUT_ASTRO_FILE + ".raw", "w") as text_file:
        text_file.write(response.text)
    os.system("jq < " + OUT_ASTRO_FILE + ".raw > " + OUT_ASTRO_FILE)
    # Remove the unformatted output file
    os.system("rm -f " + OUT_ASTRO_FILE + ".raw")

    if DEBUG: # @DEBUG
        print(80 * "-")
        print(jsonAstro)

###############################################################################
# Extract current weather data from the received data file.

def ExtractWeatherData():
    # ---------------------------------
    # Parse data for weather items

    # City & Date & time
    weatherData.city = jsonWeather["location"]["name"]
    weatherData.localtime = jsonWeather["location"]["localtime"]
    weatherData.lastupdate = jsonWeather["current"]["last_updated"]

    # Sunrise & sunset - see GetAstroInfo below

    # Temperature
    weatherData.temp = jsonWeather["current"]["temp_f"]
    # Pressure
    weatherData.inHg = jsonWeather["current"]["pressure_in"]
    weatherData.hpa = jsonWeather["current"]["pressure_mb"]
    weatherData.mmHg = inHg_to_mmHg(weatherData.inHg)
    # Humidity
    weatherData.humidity = jsonWeather["current"]["humidity"]
    # Ultraviolet index
    weatherData.uvi = jsonWeather["current"]["uv"]
    # Cloud cover (percentage)
    weatherData.clouds = jsonWeather["current"]["cloud"]
    # Wind speed and direction
    weatherData.speed = jsonWeather["current"]["wind_mph"]
    weatherData.direction = jsonWeather["current"]["wind_dir"]
    # Current conditions
    weatherData.weather = jsonWeather["current"]["condition"]["text"]
    weatherData.weatherCode = jsonWeather["current"]["condition"]["code"]
    # Precipitation
    weatherData.precip = jsonWeather["current"]["precip_in"]
    if weatherData.precip == "no":
        weatherData.precip = "None"

    # Day/night indicator
    weatherData.isDay = jsonWeather["current"]["is_day"]

    # icon = get_icon(weather)
    weatherData.icon = get_icon_from_code(weatherData.weatherCode)

    # Also extract astronomical data
    ExtractAstroData()


###############################################################################
# Extract current astronomical data from the received data file.

def ExtractAstroData():
    weatherData.sunrise = jsonAstro["astronomy"]["astro"]["sunrise"]
    weatherData.sunset = jsonAstro["astronomy"]["astro"]["sunset"]
    weatherData.moonrise = jsonAstro["astronomy"]["astro"]["moonrise"]
    weatherData.moonset = jsonAstro["astronomy"]["astro"]["moonset"]
    weatherData.phase = jsonAstro["astronomy"]["astro"]["moon_phase"]

###############################################################################

if __name__ == '__main__':
    print()
    print("This module is part of weather.py and is not meant to be executed alone.")
    print()
