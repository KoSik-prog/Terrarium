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
from lib.log import *
from lib.mainLight import *
from lib.sensors import *
from lib.heater import *
from lib.sprayer import *
from lib.display import *
from terrarium import *

class gui_CL:
    bgcolor=(0,0,0,255)
    activeTab = 0

    def __init__(self):
        display.screen.fill(self.bgcolor)

    def gui_thread(self):  #---- THREAD
        tfps=0.5

        while(terrarium.runFlag == True):
            if(self.activeTab==0):
                self.wysw()
            elif(self.activeTab==1):
                self.menu1()
            elif(self.activeTab==2):
                self.menu_sprayer()
            time.sleep(tfps)   

    def touch_thread(self):
        while(terrarium.runFlag == True):
            self.touch_event()

    def wysw(self):
        iconsPosition=5
        display.icons(0,0,255,"background")

        if(gpio.mainLightFlag == True):
            display.icons(10, iconsPosition,255,"bulb1")
            iconsPosition += 125

        if(gpio.check_heater_flag() == 1):
            display.icons(10, iconsPosition, 255,"bulb2")
            dl=display.label_center(display.screen, "{}%".format(gpio.read_heater_pwm()), "Nimbus Sans L", 48, 70, iconsPosition+50, (235, 0, 69), 255)
            iconsPosition += 125

        if(sprayer.flag == True):
            display.icons(10, iconsPosition, 255, "sprayer")
            iconsPosition += 125

        dl=display.label(display.screen, "{:.1f}°C".format(terrarium.temperatureTop),"Nimbus Sans L",150,290,10,(247,130,59),255) #(241,198,228)
        display.label(display.screen, "{:.0f}%".format(terrarium.humidityTop),"Nimbus Sans L",80,320+dl,50,(183,176,241),255)

        dl=display.label(display.screen, "{:.1f}°C".format(terrarium.temperatureBottom),"Nimbus Sans L",150,290,370,(110,254,192),255) #(206,241,198)
        display.label(display.screen, "{:.0f}%".format(terrarium.humidityBottom),"Nimbus Sans L",80,320+dl,410,(183,176,241),255)

        display.label(display.screen, "UVI:{:.4f}".format(terrarium.UVI),"Nimbus Sans L",70,430,180,(253,201,77),255)
        display.label(display.screen, "UVA: {:.2f} UVB: {:.2f}".format(terrarium.UVA,terrarium.UVB),"Nimbus Sans L",48,370,240,(254,138,35),255)

        display.label(display.screen, "{}".format(datetime.datetime.now().strftime('%H:%M:%S')),"Nimbus Sans L",60,30,420,(200,240,200),255)
        pygame.display.update()

    def menu1(self):
        end = timer()
        display.icons(0,0,255, "background")

        display.button(display.screen, (30,60,300,120) ,(223,169,191), (223,169,151), 10, 2)
        display.label(display.screen, "deszcz","Nimbus Sans L",80,90,85,(253,50,35),255)

        display.button(display.screen, (30,220,300,120) ,(216,155,43), (216,155,0), 10, 2)
        display.label(display.screen, "dripper","Nimbus Sans L",80,85,245,(253,50,35),255)

        display.button(display.screen, (360,60,300,120) ,(187,179,41), (187,179,0), 10, 2)
        display.label(display.screen, "oswietlenie","Nimbus Sans L",70,380,90,(253,50,35),255)

        display.button(display.screen, (360,220,300,120) ,(213,0,88), (213,0,38), 10, 2)
        display.label(display.screen, "wentylacja","Nimbus Sans L",70,390,250,(253,50,35),255)

        display.label(display.screen, "czas pracy:{}".format(str(datetime.timedelta(seconds = round(end - terrarium.startTime)))),"Nimbus Sans L",30,50,440,(150,150,150),100)

        display.button(display.screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
        display.label(display.screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
        pygame.display.update()

    def menu_sprayer(self):
        end = timer()
        display.icons(0, 0, 255, "background")

        if(gpio.mainLightFlag == True):
            display.icons(10,10,255,"bulb1")

        if(gpio.heaterFlag == True):
            display.icons(70,10,255,"bulb2")

        display.label(display.screen, "Timer 1: ","Nimbus Sans L",60,30,40,(253,180,165),255)
        display.button(display.screen, (200,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "-","Nimbus Sans L",90,230,0,(15,15,15),255)
        display.button(display.screen, (200,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.label(display.screen, "+","Nimbus Sans L",80,225,48,(220,220,220),255)
        display.button(display.screen, (285,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.on1H),"Nimbus Sans L",120,290,17,(220,220,220),255)
        display.label(display.screen, ":","Nimbus Sans L",120,382,15,(220,220,220),255)
        display.button(display.screen, (400,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.on1M),"Nimbus Sans L",120,405,17,(220,220,220),255)
        display.button(display.screen, (505,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "-","Nimbus Sans L",90,535,0,(15,15,15),255)
        display.button(display.screen, (505,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.label(display.screen, "+","Nimbus Sans L",80,530,48,(220,220,220),255)

        display.label(display.screen, "Timer 2: ","Nimbus Sans L",60,30,170,(253,180,165),255)
        display.button(display.screen, (200,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "-","Nimbus Sans L",90,230,130,(15,15,15),255)
        display.button(display.screen, (200,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.label(display.screen, "+","Nimbus Sans L",80,225,180,(220,220,220),255)
        display.button(display.screen, (285,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.on2H),"Nimbus Sans L",120,290,147,(220,220,220),255)
        display.label(display.screen, ":","Nimbus Sans L",120,382,145,(220,220,220),255)
        display.button(display.screen, (400,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.on2M),"Nimbus Sans L",120,405,147,(220,220,220),255)
        display.button(display.screen, (505,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "-","Nimbus Sans L",90,535,130,(15,15,15),255)
        display.button(display.screen, (505,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.label(display.screen, "+","Nimbus Sans L",80,530,178,(220,220,220),255)

        display.label(display.screen, "Czas spryskiwania: ","Nimbus Sans L",60,30,290,(253,180,165),255)
        display.button(display.screen, (420,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "-","Nimbus Sans L",110,450,264,(15,15,15),255)
        display.button(display.screen, (505,270,200,80) ,(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{} s".format(sprayer.sprayingTime),"Nimbus Sans L",80,535,280,(15,15,15),255)
        display.button(display.screen, (710,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "+","Nimbus Sans L",80,736,274,(15,15,15),255)

        display.label(display.screen, "Manualne: ","Nimbus Sans L",60,30,410,(253,180,165),255)
        display.button(display.screen, (240,380,80,50) ,(200,200,200), (250,250,250), 10, 2)
        display.label(display.screen, "-","Nimbus Sans L",90,270,370,(15,15,15),255)
        display.button(display.screen, (240,430,80,50) ,(80,80,80), (50,50,50), 10, 2)
        display.label(display.screen, "+","Nimbus Sans L",80,265,420,(220,220,220),255)
        display.button(display.screen, (325,380,200,100) ,(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{} s".format(sprayer.sprayingTimeManual),"Nimbus Sans L",80,350,400,(220,220,220),255)
        display.button(display.screen, (530,380,80,100) ,(20,192,21), (30,220,21), 10, 2)

        display.label(display.screen, "ostatnie:","Nimbus Sans L",40,670,20,(253,201,77),255)
        display.label(display.screen, "{}".format(str(datetime.timedelta(seconds=round(end - sprayer.lastSpraying)))),"Nimbus Sans L",40,670,60,(253,201,77),255)

        display.button(display.screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
        display.label(display.screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
        pygame.display.update()

    def touch_event(self):
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                terrarium.runFlag = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px=event.pos[0]
                py=event.pos[1]
                czasUruchomieniaMenu=datetime.datetime.now()
                #+++++ TOUCH EVENT ++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #--- strona 0 (glowna)----------
                if(gui.activeTab==0):
                    if(px>0 and px<400 and py>0 and py<480):
                        gui.activeTab=1
                        pygame.event.clear
                    elif(px>630 and px<800 and py>0 and py<150):
                        terrarium.runFlag = False
                        time.sleep(1)
                        pygame.quit()
                        sys.exit()
                        pygame.event.clear
                #---strona 1 (menu)-------------
                elif(gui.activeTab==1):
                    if(px>30 and px<330 and py>60 and py<180):
                        gui.activeTab=2
                        pygame.event.clear
                    elif(px>30 and px<330 and py>220 and py<340):
                        gui.activeTab=3
                        pygame.event.clear
                    elif(px>690 and px<800 and py>390 and py<480):
                        gui.activeTab=0
                        pygame.event.clear
                #---strona 2 (spryskanie)-------------
                elif(gui.activeTab==2):
                    if(px>200 and px<280 and py>10 and py<60):  #godz1 -
                        sprayer.on1H-=1
                        if(sprayer.on1H<0):
                            sprayer.on1H=23
                    if(px>200 and px<280 and py>60 and py<110): #godz1 +
                        sprayer.on1H+=1
                        if(sprayer.on1H>23):
                            sprayer.on1H=0
                    if(px>505 and px<585 and py>10 and py<60):  #min1 -
                        sprayer.on1M-=1
                        if(sprayer.on1M<0):
                            sprayer.on1M=59
                    if(px>505 and px<585 and py>60 and py<110): #min1 +
                        sprayer.on1M+=1
                        if(sprayer.on1M>59):
                            sprayer.on1M=0
                    #--------
                    if(px>200 and px<280 and py>140 and py<190):  #godz2 -
                        sprayer.on2H-=1
                        if(sprayer.on2H<0):
                            sprayer.on2H=23
                    if(px>200 and px<280 and py>190 and py<240): #godz2 +
                        sprayer.on2H+=1
                        if(sprayer.on2H>23):
                            sprayer.on2H=0
                    if(px>505 and px<585 and py>140 and py<190):  #min2 -
                        sprayer.on2M-=1
                        if(sprayer.on2M<0):
                            sprayer.on2M=59
                    if(px>505 and px<585 and py>190 and py<240): #min2 +
                        sprayer.on2M+=1
                        if(sprayer.on2M>59):
                            sprayer.on2M=0
                    #--------
                    if(px>420 and px<500 and py>270 and py<350):  #czas spryskiwania -
                        if(sprayer.sprayingTime > 5):
                            sprayer.sprayingTime -= 2
                    if(px>710 and px<790 and py>270 and py<350):  #czas spryskiwania +
                        if(sprayer.sprayingTime < 50):
                            sprayer.sprayingTime += 2
                    #--------
                    if(px>530 and px<610 and py>380 and py<480):  #spryskiwanie manualne
                        sprayer.spray_terrarium(sprayer.sprayingTime)
                        pygame.event.clear
                    if(px>240 and px<320 and py>380 and py<430): #sprysk manualne -
                        if(sprayer.sprayingTimeManual>5):
                            sprayer.sprayingTimeManual-=2
                    if(px>240 and px<320 and py>430 and py<480):  #sprysk manualne +
                        sprayer.sprayingTimeManual+=2
                    if(px>690 and px<800 and py>390 and py<480):
                        gui.activeTab=1
                #---------------------

gui = gui_CL()