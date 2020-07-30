# Node definition for a daily forecast node

try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface

import json
import time
import datetime
from nodes import et3
from nodes import uom
import node_funcs

LOGGER = polyinterface.LOGGER

@node_funcs.add_functions_as_methods(node_funcs.functions)
class DailyNode(polyinterface.Node):
    id = 'daily'
    def __init__(self, controller, primary, address, name, units):
        self.uom = uom.get_uom(units)
        self.units = units
        self.drivers = []

        # Use the units to build an appropriate drivers array.
        self.drivers.append({'driver': 'GV19', 'value': 0, 'uom': self.uom['GV19']})
        self.drivers.append({'driver': 'GV0', 'value': 0, 'uom': self.uom['GV0']})
        self.drivers.append({'driver': 'GV1', 'value': 0, 'uom': self.uom['GV1']})
        self.drivers.append({'driver': 'GV2', 'value': 0, 'uom': self.uom['GV2']})
        self.drivers.append({'driver': 'DEWPT', 'value': 0, 'uom': self.uom['DEWPT']})
        self.drivers.append({'driver': 'CLIHUM', 'value': 0, 'uom': self.uom['CLIHUM']})
        self.drivers.append({'driver': 'BARPRES', 'value': 0, 'uom': self.uom['BARPRES']})
        self.drivers.append({'driver': 'GV13', 'value': 0, 'uom': self.uom['GV13']})
        self.drivers.append({'driver': 'GV14', 'value': 0, 'uom': self.uom['GV14']})
        self.drivers.append({'driver': 'GV8', 'value': 0, 'uom': self.uom['GV8']})
        self.drivers.append({'driver': 'GV9', 'value': 0, 'uom': self.uom['GV9']})
        self.drivers.append({'driver': 'GV4', 'value': 0, 'uom': self.uom['GV4']})
        self.drivers.append({'driver': 'UV', 'value': 0, 'uom': self.uom['UV']})
        self.drivers.append({'driver': 'GV18', 'value': 0, 'uom': self.uom['GV18']})
        self.drivers.append({'driver': 'GV20', 'value': 0, 'uom': self.uom['GV20']})

        # call the default init
        super(DailyNode, self).__init__(controller, primary, address, name)


    uom = {'GV19': 25,
            'GV0': 4,
            'GV1': 4,
            'GV2': 4,
            'DEWPT': 4,
            'CLIHUM': 22,
            'BARPRES': 118,
            'GV13': 25,
            'GV14': 22,
            'GV4': 49,
            'UV': 71,
            'GV20': 107,
            'GV8': 82,
            'GV9': 82,
            'GV18': 22,
            }

    def set_driver_uom(self, units):
        self.uom = uom.get_uom(units)
        self.units = units

    def mm2inch(self, mm):
        return mm/25.4

    def update_forecast(self, forecast, latitude, elevation, plant_type, units, f):

        LOGGER.debug(forecast)
        epoch = int(forecast['dt'])
        dow = time.strftime("%w", time.localtime(epoch))
        LOGGER.info('Day of week = ' + dow)

        try:
            humidity = (forecast['Hmin'] + forecast['Hmax']) / 2
            self.update_driver('CLIHUM', round(humidity, 0), f)
            self.update_driver('BARPRES', round(forecast['pressure'], 1), f)
            self.update_driver('DEWPT', round(forecast['dewpoint'], 1), f)
            self.update_driver('GV0', round(forecast['temp_max'], 1), f)
            self.update_driver('GV1', round(forecast['temp_min'], 1), f)
            self.update_driver('GV2', round(forecast['feelslike'], 1), f)
            self.update_driver('GV14', round(forecast['clouds'], 0), f)
            self.update_driver('GV4', round(forecast['speed'], 1), f)

            self.update_driver('GV19', int(dow), f)
            self.update_driver('GV13', forecast['weather'], f)
            self.update_driver('UV', round(forecast['uv'], 1), f)
            self.update_driver('GV6', round(forecast['rain'], 2), f)
            self.update_driver('GV7', round(forecast['snow'], 2), f)
            self.update_driver('GV18', round(forecast['pop'], 0), f)
        except exception as e:
            LOGGER.error('Forecast node update failed:')
            LOGGER.error(str(e))

        # Calculate ETo
        #  Temp is in degree C and windspeed is in m/s, we may need to
        #  convert these.
        J = datetime.datetime.fromtimestamp(epoch).timetuple().tm_yday

        Tmin = forecast['temp_min']
        Tmax = forecast['temp_max']
        Ws = forecast['speed']
        if units != 'metric':
            LOGGER.info('Conversion of temperature/wind speed required')
            Tmin = et3.FtoC(Tmin)
            Tmax = et3.FtoC(Tmax)
            Ws = et3.mph2ms(Ws)

        et0 = et3.evapotranspriation(Tmax, Tmin, None, Ws, float(elevation), forecast['Hmax'], forecast['Hmin'], latitude, float(plant_type), J)
        if self.units == 'imperial':
            self.update_driver('GV20', round(self.mm2inch(et0), 3))
        else:
            self.update_driver('GV20', round(et0, 2))
        LOGGER.info("ETo = %f %f" % (et0, self.mm2inch(et0)))


