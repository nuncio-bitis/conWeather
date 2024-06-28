#!/usr/bin/env python3
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
# weather.py
#   Get weather for current location
#   This is the main file that relies on submodules to query data from a
#   server and extract weather info into a common data module (weatherData).
#   Weather icons can be customized in weatherIcons.
#
#   Usage: weather.py [-h|--help] [-d] [-f | -o] [-s | -t | -1]
#   optional arguments:
#     -h, --help Show this help message and exit
#     -d         DEBUG: Show received JSON data
#     -i         DEBUG: Show weather icons
#     -o         Use 'old' data if it's less than 15 minutes old (default)
#     -f         Force refresh of data from server
#     -s         Short output
#     -t         Tiny output
#     -1         One-liner ANSI colored
#
# J. Parziale
# 2022-02-20 Original version, using OpenWeather to get XML
# 2024-05-14 Switch to WeatherAPI to get JSON
# 2024-06-28 Create common output UI, and separate service-specific stuff.
###############################################################################
# Services:
# 1) Weather API: https://www.weatherapi.com/
# 2) OpenWeatherMap: https://openweathermap.org/api/
# 3) Open Meteo: https://open-meteo.com/ (not implemented)
###############################################################################

# @NOTE Choose which weather service module to use.
# Import service-specific API
from weatherAPI import *    # @NOTE
# from weatherOWM import *    # @NOTE

import os
import sys
import time
import getopt
import datetime

# Import weather icons
from weatherIcons import *
# Import extracted weather data
import weatherData

from colorama import Fore, Back, Style
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

###############################################################################
# Globals

DEBUG = False
SHOW_ICONS = False

# Output text
weatherInfo = []
max_width = 0

# 0 : Full
# 1 : Tiny
# 2 : Short
OUTPUT_DATA = 0

# Only query remote if data is not recent
USE_SAVED = True

# Weather data minimum refresh time, in seconds
RECENT_CHECK_SECONDS = (15.0 * 60.0)

###############################################################################

# Check if there's a saved file, and if so - was it created within the last 15 minutes.
def WeatherIsRecent():
    """Check if the saved JSON file was created recently"""

    global USE_SAVED

    # Check if the weather file exists
    if not os.path.exists(OUT_DATA_FILE):
        # No file, therefore it's not recent.
        USE_SAVED = False # Cannot use a non-existing saved file. Force refresh.
        return False

    # File exists: check if it's recent.
    now = datetime.datetime.now()

    modTime = os.path.getmtime(OUT_DATA_FILE)
    convert_time = time.localtime(modTime)
    format_time = time.strftime('%d%m%Y %H:%M:%S', convert_time)
    mod = datetime.datetime.strptime(format_time, '%d%m%Y %H:%M:%S')

    # Get difference in seconds
    diff = (now - mod).total_seconds()

    if diff > RECENT_CHECK_SECONDS:
        return False
    else:
        return True

###############################################################################

def addLine(line):
    """Add a line to the output text to be displayed"""

    global weatherInfo
    global max_width
    if (len(line) > max_width):
        max_width = len(line)
    weatherInfo.append(line)

###############################################################################
# Parse the weather data and format it to a string in a nice readable format.

def FormatFull():
    """Print weather info in a nicely-readable format."""

    addLine(f"{Style.BRIGHT}{Fore.CYAN}----------------------------------------{Style.RESET_ALL}")

    addLine(Fore.MAGENTA + LOCN + " | " + weatherData.lastupdate + Style.RESET_ALL)
    addLine(Style.BRIGHT + Fore.RED + "Temperature: " + Style.RESET_ALL + str(weatherData.temp) + u"\u00b0" + 'F')
    addLine(Fore.BLUE + "Humidity: " + Style.RESET_ALL + str(weatherData.humidity) + "%")
    addLine(Style.BRIGHT + Fore.CYAN + "Pressure: " + Style.RESET_ALL + str(weatherData.hpa) + " hPa")
    addLine("          {p:.3f} inHg".format(p=weatherData.inHg))
    addLine("          {p:.3f} mmHg".format(p=weatherData.mmHg))
    addLine(Style.BRIGHT + "Weather: " + Style.RESET_ALL + weatherData.weather + " " + weatherData.icon)
    addLine(Style.BRIGHT + "Clouds : " + Style.RESET_ALL + str(weatherData.clouds) + "%")
    addLine(Style.BRIGHT + Fore.GREEN + "Wind: " + Style.RESET_ALL \
            + str(weatherData.speed) + " mph " \
            + weatherData.direction)
    if weatherData.precip != None:
        addLine(Fore.BLUE + "Precipitation: " + Style.RESET_ALL + str(weatherData.precip) + " in")

    # Output astronomical data
    addLine(Style.BRIGHT + Fore.YELLOW + "Sun rise: " + Style.RESET_ALL + weatherData.sunrise)
    addLine(Style.BRIGHT + Fore.YELLOW + "Sun set : " + Style.RESET_ALL + weatherData.sunset)
    if weatherData.moonrise != None:
        addLine(Style.DIM + Fore.WHITE + "Moon rise: " + Style.RESET_ALL + weatherData.moonrise)
    if weatherData.moonset != None:
        addLine(Style.DIM + Fore.WHITE + "Moon set : " + Style.RESET_ALL + weatherData.moonset)
    if weatherData.phase != None:
        addLine(Fore.WHITE + "Phase : " + weatherData.phase + Style.RESET_ALL)

    addLine(f"{Style.BRIGHT}{Fore.CYAN}----------------------------------------{Style.RESET_ALL}")


###############################################################################
# Parse the weather data and format it to a string in a short format.

#|+++++++++++++|
#|Temp: xx.x°F |
#|  rH: xx%    |
#| xx.xx inHg  |
#| X mph DDD   |
#|clear sky    |
#|+++++++++++++|
def FormatShort():
    """Print weather info in a short format."""

    addLine("Temp: " + str(weatherData.temp) + "°F")
    addLine("  rH: " + str(weatherData.humidity) + "%")
    addLine(" {p:.2f} inHg".format(p=weatherData.inHg))
    addLine(" " + str(weatherData.speed) + " mph " + weatherData.direction)
    addLine(weatherData.weather)

###############################################################################
# Parse the weather data and format it to a string in a tiny format.

#|++++++++++++++++|
#|T:50.6°F  rH:52%|
#|P:29.8 inHg     |
#|++++++++++++++++|
def FormatTiny():
    """Print weather info in a tiny format."""

    addLine("T:" + str(weatherData.temp) + "°F rH:" + str(weatherData.humidity) + "%")
    addLine("P:{p:.2f}inHg".format(p=weatherData.inHg))

###############################################################################
# Parse the weather data and format it to a string in a single-line format.

def FormatOneLine():
    """Print weather info in a single-line format."""

    addLine(Style.BRIGHT + Back.BLUE
            + Fore.CYAN + weatherData.city + ": "
            + Fore.YELLOW + str(weatherData.temp) + u"\u00b0" + "F "
            + weatherData.icon + " "
            + Fore.CYAN + "Wind: "      + Fore.YELLOW + str(weatherData.speed) + " mph " + weatherData.direction + " "
            + Fore.CYAN + "Humidity: "  + Fore.YELLOW + str(weatherData.humidity) + "% "
            + Fore.CYAN + "Pressure: "  + Fore.YELLOW + "{p:.2f} inHg".format(p=weatherData.inHg) + " / "
            + "{p:.3f} mmHg".format(p=weatherData.mmHg)
            + Style.RESET_ALL)

###############################################################################

def usage():
    print("-" * 40)
    print("Usage: {:s} [-h|--help] [-d] [-f | -o] [-s | -t | -1]".format(os.path.basename(sys.argv[0])))
    print("\nPrint current weather conditions\n")
    print("optional arguments:")
    print("  -h, --help Show this help message and exit")
    print("  -d         DEBUG: Show received JSON data")
    print("  -i         DEBUG: Show weather icons")
    print("  -o         Use 'old' data if it's less than 15 minutes old (default)")
    print("  -f         Force refresh of data from server")
    print("  -s         Short output")
    print("  -t         Tiny output")
    print("  -1         One-liner ANSI colored")
    print("-" * 40)
    print()

###############################################################################

# main entry point
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdfiost1", ["help"])
    except getopt.GetoptError as err:
        # print(help information and exit:
        print(str(err)) # will print(something like "option -a not recognized"
        usage()
        sys.exit(2)

    OUTPUT_DATA = 0 # Full
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-o":
            # Don't update recent data
            USE_SAVED = True
        elif o == "-f":
            USE_SAVED = False
        elif o == "-d":
            DEBUG = True
            OUTPUT_DATA = 0 # Full format
        elif o == "-i":
            SHOW_ICONS = True
        elif o == "-t":
            OUTPUT_DATA = 1 # Tiny
        elif o == "-s":
            OUTPUT_DATA = 2 # Short
        elif o == "-1":
            OUTPUT_DATA = 3 # One-line
        else:
            print("Unhandled option: %s" % o)

    # -------------------------------------------------------------------------

    if SHOW_ICONS: # @DEBUG
        displayIcons()
        displayConditions()

    # Check if data is recent enough to re-use
    isRecent = WeatherIsRecent()

    # Get weather data from server
    GetWeatherInfo((isRecent and USE_SAVED), DEBUG)
    ExtractWeatherData()

    # -------------------------------------------------------------------------

    # Decide on output format
    if OUTPUT_DATA == 0:
        FormatFull()
    elif OUTPUT_DATA == 1:
        FormatTiny()
    elif OUTPUT_DATA == 2:
        FormatShort()
    elif OUTPUT_DATA == 3:
        FormatOneLine()
    else:
        print("Unhandled format: %d" % OUTPUT_DATA)

    # Output text
    for l in weatherInfo:
        print(l)

###############################################################################
