#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        terrarium
#
# Author:      KoSik
#
# Created:     27.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    import json
    from timeit import default_timer as timer
except ImportError:
    print("Import error - terrarium")


class Terrarium:
    temperatureTop = 0.0
    humidityTop = 0.0
    temperatureBottom = 0.0
    humidityBottom = 0.0
    uva = 0.0
    uvb = 0.0
    uvi = 0.0
    socked_message_interval = 5
    minimumHumidity = 50
    temperatureRequiredIsland = 29.0
    spraysToday = 0
    # UV index at which the heating turns on / does not turn on when the chameleon covers the sensor
    minUviForHeating = 0.15
    runFlag = True  # flag keeping the main threads
    startTime = 0

    def __init__(self):
        self.sensorsLastUpdateTime = datetime.datetime.now()
        self.mainLightLastUpdateTime = datetime.datetime.now()
        self.heaterLastUpdateTime = datetime.datetime.now()
        self.startTime = timer()
        self.lastWatchdogResetTime = datetime.datetime.now()

    def get_requred_island_temperature(self):
        return self.temperatureRequiredIsland
    
    def get_minimum_humidity(self):
        return terrarium.minimumHumidity
    
    def get_min_uvi_for_heating(self):
        return terrarium.minUviForHeating
    
    def set_requred_island_temperature(self, temp):
        self.temperatureRequiredIsland = temp
        
    def set_minimum_humidity(self, humi):
        terrarium.minimumHumidity = humi
    
    def set_min_uvi_for_heating(self, uvi):
        terrarium.minUviForHeating = uvi
        
    def get_socket_message_interval(self):
        return self.socked_message_interval

    def get_socket_message(self):
        dataList = {"tempTop":round(self.temperatureTop, 1), "humiTop":round(self.humidityTop, 0), "tempBottom":round(self.temperatureBottom, 1), "humiBottom":round(self.humidityBottom, 0), "uvi":round(self.uvi, 2), "spraysToday":self.spraysToday}
        return "setTerrariumData.{}".format(json.dumps(dataList))


terrarium = Terrarium()
