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
    tempG = 0.0
    wilgG = 0.0
    tempD = 0.0
    wilgD = 0.0
    UVA = 0.0
    UVB = 0.0
    UVI = 0.0
    czasWyslania = 0
    interwalWysylania = 5
    minWilgotnosc = 50
    tempWymaganaNaWyspie = 29.0 #temp wymagana na wyspie
    minUVIdlaOgrzewania = 0.15 #index UVI przy ktorym zalacza sie ogrzewanie / nie zalacza gdy kameleon zaslania czujnik
    ostatnieOdswiezenieCzujnikow = 0 #czas w ktorym ostatni raz czujniki daly dobry odczyt
    staraTempG = 0.0
    staraWilgG = 0.0
    staraTempD = 0.0
    staraWilgD = 0.0
    staraUVA = 0.0
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
        
terrarium = terrariumCl