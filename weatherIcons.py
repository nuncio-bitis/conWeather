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
# Unicode Symbols for weather icons, including ANSI colors

iconSun          = b"\033[33;1m\xe2\x98\x80 ".decode("utf-8")
iconMoon         = b"\033[37;1m\xe2\x98\xbd ".decode("utf-8")
iconClouds       = b"\033[37;1m\xe2\x98\x81 ".decode("utf-8")
iconRain         = b"\033[34;1m\xe2\x98\x94 ".decode("utf-8")
# iconFog          = b"\033[37;1m\xe2\x96\x92 ".decode("utf-8")
iconFog          = "\033[37;1m\U0001f32b "
iconMist         = b"\033[34;1m\xe2\x96\x91 ".decode("utf-8")
iconHaze         = b"\033[33;1m\xe2\x96\x91 ".decode("utf-8")
iconSnow         = b"\033[37;1m\xe2\x9d\x84 ".decode("utf-8")
iconThunderstorm = b"\033[33;1m\xe2\x9a\xa1 ".decode("utf-8")
iconTornado      = "\033[33;1m\U0001f32a "
iconSquall       = "\033[33;1m\U0001f32c "

# For debugging
def displayIcons():
    print("sun = " + iconSun + " \033[0m")
    print("moon = " + iconMoon + " \033[0m")
    print("clouds = " + iconClouds + " \033[0m")
    print("rain = " + iconRain + " \033[0m")
    print("fog = " + iconFog + " \033[0m")
    print("mist = " + iconMist + " \033[0m")
    print("haze = " + iconHaze + " \033[0m")
    print("snow = " + iconSnow + " \033[0m")
    print("thunderstorm = " + iconThunderstorm + " \033[0m")
    print("tornado = " + iconTornado + " \033[0m")
    print("squall = " + iconSquall + " \033[0m")

def get_icon(condition, isDay):
    if condition == "Clear" or condition == "Sunny":
        if isDay:
            return iconSun
        else:
            return iconMoon
    elif condition == "Clouds" or condition == "Partly cloudy":
        return iconClouds
    elif condition == "Rain":
        return iconRain
    elif condition == "Fog":
        return iconFog
    elif condition == "Mist":
        return iconMist
    elif condition == "Haze":
        return iconHaze
    elif condition == "Snow":
        return iconSnow
    elif condition == "Thunderstorm":
        return iconThunderstorm
    elif condition == "Tornado":
        return iconTornado
    elif condition == "Squall":
        return iconSquall
    else:
        print("ERROR: No icon found for " + condition)
        return ""

###############################################################################

if __name__ == '__main__':
    print()
    print("This module is part of weather.py and is not meant to be executed alone.")
    print()
