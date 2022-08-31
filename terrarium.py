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

class terrariumCl:   #TERRARIUM
    temperatureTop = 0.0
    humidityTop = 0.0
    temperatureBottom = 0.0
    humidityBottom = 0.0
    UVA = 0.0
    UVB = 0.0
    UVI = 0.0
    socked_message_interval = 5
    minimumHumidity = 50
    temperature_required_island = 29.0 #temp wymagana na wyspie
    minUviForHeating = 0.15 #index UVI przy ktorym zalacza sie ogrzewanie / nie zalacza gdy kameleon zaslania czujnik
    #czasOczekiwaniaNaCzujniki = 90   #w minutach oczekiwanie na zmianę wartosci czujnikow (dla wykrywania bledow)
    runFlag = True #flaga utrzymujaca watki
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
        
terrarium = terrariumCl()