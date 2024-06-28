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
# Conversions for weather data

import datetime

def hPa_to_inHg(hPa):
    """Convert from hectoPascals to inches of mercury"""
    return (float(hPa) * 0.02953)

def inHg_to_mmHg(inHg):
    """Convert from inches of mercury to millimeters of mercury"""
    return (float(inHg) * 25.4)

def seconds_to_local(utc_time):
    """Convert time from UTC to local"""
    # Output YYYY-mm-dd HH:MM
    dateTime = datetime.datetime.fromtimestamp(utc_time)
    return dateTime.strftime("%F %I:%M %p")

def seconds_to_time(utc_time):
    """Convert time from UTC to local time"""
    # Output HH:MM
    dateTime = datetime.datetime.fromtimestamp(utc_time)
    return dateTime.strftime("%I:%M %p")

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

###############################################################################
