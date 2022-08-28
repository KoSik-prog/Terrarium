#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GUI
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
from libraries.log import *
from libraries.mainLight import *
from libraries.sensors import *
from libraries.heater import *
from libraries.sprayer import *
from libraries.display import *
from terrarium import *

class gui_CL:
    bgcolor=(0,0,0,255)
    aktywnaStrona = 0

    def __init__(self):
        display.screen.fill(self.bgcolor)

    def gui_thread(self):  #----WYSWIETLANIE - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
        tfps=0.5

        while(terrarium.runFlag == True):
            if(self.aktywnaStrona==0):
                self.wysw()
            elif(self.aktywnaStrona==1):
                self.menu1()
            elif(self.aktywnaStrona==2):
                self.menuSpryskiwacz()
            time.sleep(tfps)   

    def wysw(self):
        pozycjaIkon=5
        display.icons(0,0,255,"tlo")

        if(mainLight.flag == 1):
            display.icons(10, pozycjaIkon,255,"zarowka1")
            pozycjaIkon += 125

        if(heater.flag == 1):
            display.icons(10, pozycjaIkon, 255,"zarowka2")
            dl=display.napis_centralny(display.screen, "{}%".format(heater.pwm), "Nimbus Sans L", 48, 70, pozycjaIkon+50, (235, 0, 69), 255)
            pozycjaIkon += 125

        if(sprayer.flaga == True):
            display.icons(10, pozycjaIkon, 255, "spryskiwacz")
            pozycjaIkon += 125

        dl=display.napis(display.screen, "{:.1f}°C".format(terrarium.tempG),"Nimbus Sans L",150,290,10,(247,130,59),255) #(241,198,228)
        display.napis(display.screen, "{:.0f}%".format(terrarium.wilgG),"Nimbus Sans L",80,320+dl,50,(183,176,241),255)

        dl=display.napis(display.screen, "{:.1f}°C".format(terrarium.tempD),"Nimbus Sans L",150,290,370,(110,254,192),255) #(206,241,198)
        display.napis(display.screen, "{:.0f}%".format(terrarium.wilgD),"Nimbus Sans L",80,320+dl,410,(183,176,241),255)

        display.napis(display.screen, "UVI:{:.4f}".format(terrarium.UVI),"Nimbus Sans L",70,430,180,(253,201,77),255)
        display.napis(display.screen, "UVA: {:.2f} UVB: {:.2f}".format(terrarium.UVA,terrarium.UVB),"Nimbus Sans L",48,370,240,(254,138,35),255)

        display.napis(display.screen, "{}".format(datetime.datetime.now().strftime('%H:%M:%S')),"Nimbus Sans L",60,30,420,(200,240,200),255)
        pygame.display.update()

    def menu1(self):
        end = timer()
        display.icons(0,0,255,"tlo")

        display.przycisk(display.screen, (30,60,300,120) ,(223,169,191), (223,169,151), 10, 2)
        display.napis(display.screen, "deszcz","Nimbus Sans L",80,90,85,(253,50,35),255)

        display.przycisk(display.screen, (30,220,300,120) ,(216,155,43), (216,155,0), 10, 2)
        display.napis(display.screen, "dripper","Nimbus Sans L",80,85,245,(253,50,35),255)

        display.przycisk(display.screen, (360,60,300,120) ,(187,179,41), (187,179,0), 10, 2)
        display.napis(display.screen, "oswietlenie","Nimbus Sans L",70,380,90,(253,50,35),255)

        display.przycisk(display.screen, (360,220,300,120) ,(213,0,88), (213,0,38), 10, 2)
        display.napis(display.screen, "wentylacja","Nimbus Sans L",70,390,250,(253,50,35),255)

        display.napis(display.screen, "czas pracy:{}".format(str(datetime.timedelta(seconds = round(end - terrarium.startTime)))),"Nimbus Sans L",30,50,440,(150,150,150),100)

        display.przycisk(display.screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
        display.napis(display.screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
        pygame.display.update()

    def menuSpryskiwacz(self):
        end = timer()
        display.icons(0,0,255,"tlo")

        if(mainLight.flag == True):
            display.icons(10,10,255,"zarowka1")

        if(heater.flag == True):
            display.icons(70,10,255,"zarowka2")

        display.napis(display.screen, "Timer 1: ","Nimbus Sans L",60,30,40,(253,180,165),255)
        display.przycisk(display.screen, (200,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "-","Nimbus Sans L",90,230,0,(15,15,15),255)
        display.przycisk(display.screen, (200,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.napis(display.screen, "+","Nimbus Sans L",80,225,48,(220,220,220),255)
        display.przycisk(display.screen, (285,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.napis(display.screen, "{:02d}".format(sprayer.on1H),"Nimbus Sans L",120,290,17,(220,220,220),255)
        display.napis(display.screen, ":","Nimbus Sans L",120,382,15,(220,220,220),255)
        display.przycisk(display.screen, (400,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.napis(display.screen, "{:02d}".format(sprayer.on1M),"Nimbus Sans L",120,405,17,(220,220,220),255)
        display.przycisk(display.screen, (505,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "-","Nimbus Sans L",90,535,0,(15,15,15),255)
        display.przycisk(display.screen, (505,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.napis(display.screen, "+","Nimbus Sans L",80,530,48,(220,220,220),255)

        display.napis(display.screen, "Timer 2: ","Nimbus Sans L",60,30,170,(253,180,165),255)
        display.przycisk(display.screen, (200,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "-","Nimbus Sans L",90,230,130,(15,15,15),255)
        display.przycisk(display.screen, (200,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.napis(display.screen, "+","Nimbus Sans L",80,225,180,(220,220,220),255)
        display.przycisk(display.screen, (285,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.napis(display.screen, "{:02d}".format(sprayer.on2H),"Nimbus Sans L",120,290,147,(220,220,220),255)
        display.napis(display.screen, ":","Nimbus Sans L",120,382,145,(220,220,220),255)
        display.przycisk(display.screen, (400,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.napis(display.screen, "{:02d}".format(sprayer.on2M),"Nimbus Sans L",120,405,147,(220,220,220),255)
        display.przycisk(display.screen, (505,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "-","Nimbus Sans L",90,535,130,(15,15,15),255)
        display.przycisk(display.screen, (505,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.napis(display.screen, "+","Nimbus Sans L",80,530,178,(220,220,220),255)

        display.napis(display.screen, "Czas spryskiwania: ","Nimbus Sans L",60,30,290,(253,180,165),255)
        display.przycisk(display.screen, (420,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "-","Nimbus Sans L",110,450,264,(15,15,15),255)
        display.przycisk(display.screen, (505,270,200,80) ,(55,112,21), (55,112,21), 10, 2)
        display.napis(display.screen, "{} s".format(sprayer.czasSpryskiwania),"Nimbus Sans L",80,535,280,(15,15,15),255)
        display.przycisk(display.screen, (710,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "+","Nimbus Sans L",80,736,274,(15,15,15),255)

        display.napis(display.screen, "Manualne: ","Nimbus Sans L",60,30,410,(253,180,165),255)
        display.przycisk(display.screen, (240,380,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.napis(display.screen, "-","Nimbus Sans L",90,270,370,(15,15,15),255)
        display.przycisk(display.screen, (240,430,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.napis(display.screen, "+","Nimbus Sans L",80,265,420,(220,220,220),255)
        display.przycisk(display.screen, (325,380,200,100) ,(55,112,21), (55,112,21), 10, 2)
        display.napis(display.screen, "{} s".format(sprayer.czasSpryskManual),"Nimbus Sans L",80,350,400,(220,220,220),255)
        display.przycisk(display.screen, (530,380,80,100) ,(20,192,21), (30,220,21), 10, 2)

        display.napis(display.screen, "ostatnie:","Nimbus Sans L",40,670,20,(253,201,77),255)
        display.napis(display.screen, "{}".format(str(datetime.timedelta(seconds=round(end - sprayer.ostatnieSpryskanie)))),"Nimbus Sans L",40,670,60,(253,201,77),255)

        display.przycisk(display.screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
        display.napis(display.screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
        pygame.display.update()

gui = gui_CL()