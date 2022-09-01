#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        terrarium
#
# Author:      KoSik
#
# Created:     27.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import datetime
from timeit import default_timer as timer

class Terrarium:
    temperatureTop = 0.0
    humidityTop = 0.0
    temperatureBottom = 0.0
    humidityBottom = 0.0
    UVA = 0.0
    UVB = 0.0
    UVI = 0.0
    socked_message_interval = 5
    minimumHumidity = 50
    temperature_required_island = 29.0
    minUviForHeating = 0.15 #UV index at which the heating turns on / does not turn on when the chameleon covers the sensor
    runFlag = True #flag keeping the main threads
    startTime = 0

    sensorsLastUpdateTime = 0
    mainLightLastUpdateTime = 0
    heaterLastUpdateTime = 0

    def __init__(self):
        self.sensorsLastUpdateTime = datetime.datetime.now()
        self.mainLightLastUpdateTime = datetime.datetime.now()
        self.heaterLastUpdateTime = datetime.datetime.now()
        self.startTime = timer()

    def read_requred_island_temperature(self):
        return self.temperature_required_island

    def read_socket_message_interval(self):
        return self.socked_message_interval

    def return_socket_message(self):
        return "terrarium.T:{:4.1f}/W:{:3.0f},t:{:4.1f}/w:{:3.0f}/I:{:9.4f}".format(self.temperatureTop, self.humidityTop, self.temperatureBottom, self.humidityBottom, self.UVI)
        
terrarium = Terrarium()