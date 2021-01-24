
# OpenWeatherMaps

This is a node server to pull weather data from OpenWeatherMaps and make it available to a [Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2)

OpenWeatherMaps requires you to create an API key that you will need to access the data via their API.  See [OpenWeatherMap](http://openweathermap.org/api)

(c) 2018 Robert Paauwe
MIT license.


## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install.
3. Add NodeServer in Polyglot Web
   * After the install completes, Polyglot will reboot your ISY, you can watch the status in the main polyglot log.
4. Once your ISY is back up open the Admin Console.
5. Configure the node server per configuration section below.

### Node Settings
The settings for this node are:

#### Short Poll
   * How often to poll the OpenWeatherMap weather service. Note that the data is only updated every 10 minutes. Setting this to less may result in exceeding the free service rate limit.
#### Long Poll
   * not used

#### APIkey   
	* Your API ID, needed to authorize connection to the OpenWeatherMap API.

#### Units
	* 'metric' or 'imperial' request data in this units format.

#### Location
    * by coordinates (lat=xx&lon=xxx)

#### Forecast Days
	* The number of forecast nodes to create and populate. The range is 0 to 8.

#### Elevation
	* Height above sea level, in meters, for the location specified above. 

#### Plant Type
	* Crop coefficent for evapotranspiration calculation. Default is 0.23

## Node substituion variables
### Current condition node
 * sys.node.[address].ST      (Node sever online)
 * sys.node.[address].CLITEMP (current temperature)
 * sys.node.[address].CLIHUM  (current humidity)
 * sys.node.[address].BARPRES (current barometric pressure)
 * sys.node.[address].WINDDIR (current wind direction )
 * sys.node.[address].DISTANC (current visibility)
 * sys.node.[address].DEWPT   (current dew point temperature)
 * sys.node.[address].UV      (current UV index)
 * sys.node.[address].GV2     (current feels like temperature)
 * sys.node.[address].GV4     (current wind speed)
 * sys.node.[address].GV6     (current rain rate)
 * sys.node.[address].GV7     (current snow rate)
 * sys.node.[address].GV13    (current conditions)
 * sys.node.[address].GV14    (current percent cloud coverage)
 * sys.node.[address].GV18    (current percent chance of precipitation)

 ### Forecast node
 * sys.node.[address].CLIHUM  (forecasted humidity)
 * sys.node.[address].BARPRES (forecasted barometric pressure)
 * sys.node.[address].DEWPT   (forecasted dew point temperature)
 * sys.node.[address].UV      (forecasted max UV index)
 * sys.node.[address].GV19    (day of week forecast is for)
 * sys.node.[address].GV0     (forecasted high temperature)
 * sys.node.[address].GV1     (forecasted low temperature)
 * sys.node.[address].GV2     (forecasted daytime feels like temperature)
 * sys.node.[address].GV13    (forecasted conditions)
 * sys.node.[address].GV14    (forecasted percent cloud coverage)
 * sys.node.[address].GV4     (forecasted wind speed)
 * sys.node.[address].GV6     (forecasted rain)
 * sys.node.[address].GV7     (forecasted snow)
 * sys.node.[address].GV18    (forecasted percent chance of precipitation)
 * sys.node.[address].GV20    (calculated ETo for the day)

## Requirements

1. Polyglot V2 itself should be run on Raspian Stretch.
  To check your version, ```cat /etc/os-release``` and the first line should look like
  ```PRETTY_NAME="Raspbian GNU/Linux 9 (stretch)"```. It is possible to upgrade from Jessie to
  Stretch, but I would recommend just re-imaging the SD card.  Some helpful links:
   * https://www.raspberrypi.org/blog/raspbian-stretch/
   * https://linuxconfig.org/raspbian-gnu-linux-upgrade-from-jessie-to-raspbian-stretch-9
2. This has only been tested with ISY 5.0.14 so it is not guaranteed to work with any other version.

# Upgrading

Open the Polyglot web page, go to nodeserver store and click "Update" for "WeatherFlow".

For Polyglot 2.0.35, hit "Cancel" in the update window so the profile will not be updated and ISY rebooted.  The install procedure will properly handle this for you.  This will change with 2.0.36, for that version you will always say "No" and let the install procedure handle it for you as well.

Then restart the nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

The nodeserver keeps track of the version number and when a profile rebuild is necessary.  The profile/version.txt will contain the profile_version which is updated in server.json when the profile should be rebuilt.

# Release Notes

- 3.0.1 01/24/2021
   - Convert probablity of precipitation to percent chance of preciptitation
   - Add notice if location doesn't look like lat/long
   - Fix location example
- 3.0.0 07/30/2020
   - Replaced API calls with new OpenWeatherMap OnCall API call.
     This provides better daily forecast data.
- 2.0.3 06/10/2020
   - Add inches/day to the ET node value
- 2.0.2 03/17/2020
   - Fix syntax error in discover
- 2.0.1 03/16/2020
   - Add requests to the requirements
   - Set a default for location
   - Add Forecast Days parameter info
   - Add node sustitution variables info to docs
   - Limit Forecast Days to 5
   - Check that forecast data actually exist before trying to use it
   - Clean up forecast data nodes
   - Add wind gust to current conditions
   - Change "Rain Today" to "Rain 1/3hr" 
- 2.0.0 01/13/2020
   - Redesign node server to make more module
   - Add control to select logging level
   - Add snow data
   - Configurable number of forecast days
   - Fix rain today data
   - Change how custom parameters are maintained
- 1.2.8 11/25/2019
   - Trap failures in http requests.
- 1.2.7 09/15/2019
   - Fix use of uninitalized uv data when no uv data exist.
- 1.2.6 09/06/2019
   - Trap no dat return from uv query.
- 1.2.5 08/27/2019
   - Fix use of uninitialized uv data.
- 1.2.4 08/20/2019
   - Add error check on location data.
- 1.2.3 08/19/2019
   - Add error check on forecast UV data.
- 1.2.2 08/15/2019
   - Improve error checkin, specifically for wind direction.
- 1.2.1 08/03/2019
   - Allow zipcode without country code for backwards compatibility
- 1.2.0 08/03/2019
   - Add some additional error checking to queried values
   - Allow for city, lat/long location specifiers in configuration
- 1.1.1 07/30/2019
   - Fix condition codes editor entry and NSL entries.
- 1.1.0 07/17/2019
   - Rewrite editor profile and node server code to make use of multi-uom
     editors.  This seems to be a better way to handle switching between
     imperial and metric units.
- 1.0.1 07/12/2019
   - Fix errors in editor profile file
- 1.0.0 03/05/2019
   - Initial version published to github
