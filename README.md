# conWeather

## Description

conWeather is a set of Python scripts for displaying the current weather conditions in your terminal, including ANSI colors and Unicode weather icons.

Screenshot of full (default) weather conditions:

![conWeather Screenshot - Full][1]

Screenshot of short-style weather conditions:

![conWeather Screenshot - Short][2]

Screenshot of tiny-style weather conditions:

![conWeather Screenshot - Tiny][3]

Screenshot of one-liner weather conditions:

![conWeather Screenshot - One-Liner][4]

Weather data is queried from a weather API of your choosing.
You need to modify the service-specific files to add your API key
and implement the get request and extract the data from the response.

Currently-supported weather APIs:

* [`OpenWeatherMap`][6] free weather API (weatherOWM.py)
* [`WeatherAPI`][7] free weather API (weatherAPI.py)

## Requirements

conWeather requires the following dependencies:

* An API key for the weather service of your choice.
* THe GPS coordinates of your location.
* A command to fetch HTTP data such as FTP, cURL or wget.
* [jq][5] (lightweight and flexible command-line JSON processor)
* The Python `colorama` library for ANSI colors.

## Installation

1) Clone the repository  
2) Update your location info in weatherLocation.py
3) Add your API key(s) to weatherAPI.py, weatherOWM.py, etc. A generic key already exists in weatherOWM.py
4) Invoke the script by typing:  
    ./weather.py

## Usage

### Synopsis

    Usage: weather.py [-h|--help] [-d] [-f | -o] [-s | -t | -1]

### Options

    -h, --help Show this help message and exit
    -d         DEBUG: Show received JSON data
    -i         DEBUG: Show weather icons
    -o         Use 'old' data if it's less than 15 minutes old (default)
    -f         Force refresh of data from server
    -s         Short output
    -t         Tiny output
    -1         One-liner ANSI colored

## Configuration

* weatherLocation.py : Update the GPS coordinates for your location.
* weatherIcons.py : You can customize the Unicode weather icons here.
* weatherAPI.py : Update the API key for the WeatherAPI service
* weatherOWM.py : Update the API key for the OpenWeatherMap service
* weather.py: Modify the import to use your preferred service.

### API key

Specify an API key in the files described above. By default conWeather
uses a key for OpenWeatherMap, but users can optionally get their own
by creating a free [OpenWeatherMap account][8].

    API_KEY="85a4e3c55b73909f42c6a23ec35b7147"

## License

AnsiWeather is released under the MIT license. See `LICENSE` file
for details.

## Author

conWeather is developed by Nuncio Bitis (aka Jim Parziale).

## Resources

GitHub: https://github.com/nuncio-bitis/conWeather

[1]: https://github.com/nuncio-bitis/conWeather/screenshot-full.png
[2]: https://github.com/nuncio-bitis/conWeather/screenshot-short.png
[3]: https://github.com/nuncio-bitis/conWeather/screenshot-tiny.png
[4]: https://github.com/nuncio-bitis/conWeather/screenshot-1line.png

[5]: https://stedolan.github.io/jq/
[6]: https://openweathermap.org/api/
[7]: https://www.weatherapi.com/
[8]: https://home.openweathermap.org/users/sign_up
