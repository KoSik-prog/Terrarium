#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        terrarium main program
# Purpose:
#
# Author:      KoSik
#
# Created:     06.08.2020
# Copyright:   (c) kosik 2020
#-------------------------------------------------------------------------------
import pygame, pygame.mixer, pygame.gfxdraw, glob, time, sys, datetime, smbus, board, busio, adafruit_veml6075, socket, threading, os, ekran
import RPi.GPIO as GPIO
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
import xml.etree.cElementTree as ET

from timeit import default_timer as timer

from libraries.log import *
from libraries.mainLight import *
from libraries.sensors import *
from libraries.heater import *
from libraries.sprayer import *
from terrarium import *
#+++++++ZMIENNE++++++++++++++++++++++++++++++++++++++
bgcolor=(0,0,0,255)
kolorczcionki=(185,242,107,255)
tfps=1

serverAddressPort = ("192.168.0.99", 2222)
bufferSize = 1024

aktywnaStrona=0 #strona do wyswietlenia
#+++++++++++++++++++++ ZWLOKA CZASOWA +++++++++++++++++++++++++++
time.sleep(10)

mainLight = MAIN_LIGHT_CL(19, '8:00:00.0000', '19:15:00.0000')
#+++++++++++++++++++++++++++++WE/WY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GPIO.setmode(GPIO.BCM)
#GPIO.setup(12, GPIO.OUT) #dripper ENABLE pin
#GPIO.setup(20, GPIO.OUT) #dripper STEP
#GPIO.setup(16, GPIO.OUT) #dripper DIR
######################################################################################
def wysw_init():
    global screen

    pygame.init()
    resolution = 800,480
    #screen = pygame.display.set_mode(resolution,FULLSCREEN)
    screen = pygame.display.set_mode(resolution, 1)
    pygame.display.set_caption('Terrarium')
    screen.fill(bgcolor)
    pygame.mouse.set_cursor((8,8), (0,0), (0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))

#inicjalizacja ekranu!!!!!!!!!!!!!!!
wysw_init()

def wysw():
    global screen
    pozycjaIkon=5

    ekran.icons(0,0,255,"tlo")

    if(mainLight.flag == 1):
        ekran.icons(10, pozycjaIkon,255,"zarowka1")
        pozycjaIkon += 125

    if(heater.flag == 1):
        ekran.icons(10, pozycjaIkon, 255,"zarowka2")
        dl=ekran.napis_centralny(screen, "{}%".format(heater.pwm), "Nimbus Sans L", 48, 70, pozycjaIkon+50, (235, 0, 69), 255)
        pozycjaIkon += 125

    if(sprayer.flaga == True):
        ekran.icons(10, pozycjaIkon, 255, "spryskiwacz")
        pozycjaIkon += 125

    dl=ekran.napis(screen, "{:.1f}°C".format(terrarium.tempG),"Nimbus Sans L",150,290,10,(247,130,59),255) #(241,198,228)
    ekran.napis(screen, "{:.0f}%".format(terrarium.wilgG),"Nimbus Sans L",80,320+dl,50,(183,176,241),255)

    dl=ekran.napis(screen, "{:.1f}°C".format(terrarium.tempD),"Nimbus Sans L",150,290,370,(110,254,192),255) #(206,241,198)
    ekran.napis(screen, "{:.0f}%".format(terrarium.wilgD),"Nimbus Sans L",80,320+dl,410,(183,176,241),255)

    ekran.napis(screen, "UVI:{:.4f}".format(terrarium.UVI),"Nimbus Sans L",70,430,180,(253,201,77),255)
    ekran.napis(screen, "UVA: {:.2f} UVB: {:.2f}".format(terrarium.UVA,terrarium.UVB),"Nimbus Sans L",48,370,240,(254,138,35),255)

    ekran.napis(screen, "{}".format(datetime.datetime.now().strftime('%H:%M:%S')),"Nimbus Sans L",60,30,420,(200,240,200),255)
    pygame.display.update()

def menu1():
    global screen

    end = timer()
    ekran.icons(0,0,255,"tlo")

    ekran.przycisk(screen, (30,60,300,120) ,(223,169,191), (223,169,151), 10, 2)
    ekran.napis(screen, "deszcz","Nimbus Sans L",80,90,85,(253,50,35),255)

    ekran.przycisk(screen, (30,220,300,120) ,(216,155,43), (216,155,0), 10, 2)
    ekran.napis(screen, "dripper","Nimbus Sans L",80,85,245,(253,50,35),255)

    ekran.przycisk(screen, (360,60,300,120) ,(187,179,41), (187,179,0), 10, 2)
    ekran.napis(screen, "oswietlenie","Nimbus Sans L",70,380,90,(253,50,35),255)

    ekran.przycisk(screen, (360,220,300,120) ,(213,0,88), (213,0,38), 10, 2)
    ekran.napis(screen, "wentylacja","Nimbus Sans L",70,390,250,(253,50,35),255)

    ekran.napis(screen, "czas pracy:{}".format(str(datetime.timedelta(seconds = round(end - terrarium.startTime)))),"Nimbus Sans L",30,50,440,(150,150,150),100)

    ekran.przycisk(screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
    ekran.napis(screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
    pygame.display.update()

def menuSpryskiwacz():
    global screen

    end = timer()
    ekran.icons(0,0,255,"tlo")

    if(mainLight.flag == True):
        ekran.icons(10,10,255,"zarowka1")

    if(heater.flag == True):
        ekran.icons(70,10,255,"zarowka2")

    ekran.napis(screen, "Timer 1: ","Nimbus Sans L",60,30,40,(253,180,165),255)
    ekran.przycisk(screen, (200,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,230,0,(15,15,15),255)
    ekran.przycisk(screen, (200,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,225,48,(220,220,220),255)
    ekran.przycisk(screen, (285,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(sprayer.on1H),"Nimbus Sans L",120,290,17,(220,220,220),255)
    ekran.napis(screen, ":","Nimbus Sans L",120,382,15,(220,220,220),255)
    ekran.przycisk(screen, (400,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(sprayer.on1M),"Nimbus Sans L",120,405,17,(220,220,220),255)
    ekran.przycisk(screen, (505,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,535,0,(15,15,15),255)
    ekran.przycisk(screen, (505,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,530,48,(220,220,220),255)

    ekran.napis(screen, "Timer 2: ","Nimbus Sans L",60,30,170,(253,180,165),255)
    ekran.przycisk(screen, (200,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,230,130,(15,15,15),255)
    ekran.przycisk(screen, (200,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,225,180,(220,220,220),255)
    ekran.przycisk(screen, (285,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(sprayer.on2H),"Nimbus Sans L",120,290,147,(220,220,220),255)
    ekran.napis(screen, ":","Nimbus Sans L",120,382,145,(220,220,220),255)
    ekran.przycisk(screen, (400,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(sprayer.on2M),"Nimbus Sans L",120,405,147,(220,220,220),255)
    ekran.przycisk(screen, (505,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,535,130,(15,15,15),255)
    ekran.przycisk(screen, (505,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,530,178,(220,220,220),255)

    ekran.napis(screen, "Czas spryskiwania: ","Nimbus Sans L",60,30,290,(253,180,165),255)
    ekran.przycisk(screen, (420,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",110,450,264,(15,15,15),255)
    ekran.przycisk(screen, (505,270,200,80) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{} s".format(sprayer.czasSpryskiwania),"Nimbus Sans L",80,535,280,(15,15,15),255)
    ekran.przycisk(screen, (710,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,736,274,(15,15,15),255)

    ekran.napis(screen, "Manualne: ","Nimbus Sans L",60,30,410,(253,180,165),255)
    ekran.przycisk(screen, (240,380,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,270,370,(15,15,15),255)
    ekran.przycisk(screen, (240,430,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,265,420,(220,220,220),255)
    ekran.przycisk(screen, (325,380,200,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{} s".format(sprayer.czasSpryskManual),"Nimbus Sans L",80,350,400,(220,220,220),255)
    ekran.przycisk(screen, (530,380,80,100) ,(20,192,21), (30,220,21), 10, 2)

    ekran.napis(screen, "ostatnie:","Nimbus Sans L",40,670,20,(253,201,77),255)
    ekran.napis(screen, "{}".format(str(datetime.timedelta(seconds=round(end - sprayer.ostatnieSpryskanie)))),"Nimbus Sans L",40,670,60,(253,201,77),255)

    ekran.przycisk(screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
    ekran.napis(screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
    pygame.display.update()

def LCD():  #----WYSWIETLANIE - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
    global aktywnaStrona
    tfps=0.5

    while(terrarium.runFlag == True):
        if(aktywnaStrona==0):
            wysw()
        elif(aktywnaStrona==1):
            menu1()
        elif(aktywnaStrona==2):
            menuSpryskiwacz()
        time.sleep(tfps)

def zapis_ustawien_xml():
    setings = ET.Element("settings")

    ET.SubElement(setings, "minWilgotnosc").text = str(terrarium.minWilgotnosc)

    tree2 = ET.ElementTree(setings)
    tree2.write('Desktop/terra/ustawienia.xml')
    log.add_log("Zapisano ustawienia")

def odczyt_ustawien_xml():
    tree = ET.ElementTree(file='Desktop/terra/ustawienia.xml')
    root = tree.getroot()

    terrarium.minWilgotnosc = int(root.find('minWilgotnosc').text)
#++++++++++++++++ THREADS DEFINISIONS ++++++++++++++++++++++++++++++++++++++++++++++++++
def thread_sensors_init():
    sensorsTH = threading.Thread(target = sensors.sensors_thread)
    sensorsTH.start()

def thread_main_light_init():
    mainLightTH = threading.Thread(target = mainLight.mainLightThread)
    mainLightTH.start()

def thread_heater_init():
    heaterTH = threading.Thread(target = heater.heaterThread)
    heaterTH.start()

def thread_heater_pwm_control_init():
    heaterPwmControlTH = threading.Thread(target = heater.pwmControlThread)
    heaterPwmControlTH.start()

def thread_sprayer_init():
    sprayerTH = threading.Thread(target = sprayer.sprayer_thread)
    sprayerTH.start()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    global aktywnaStrona

    log.add_log("Starting...")

    terrarium.licznikOczekiwaniaNaCzujniki=120*60
    terrarium.ostatnieOdswiezenieCzujnikow = datetime.datetime.now()

    zapis_ustawien_xml()
    odczyt_ustawien_xml()
    #-------------THREADS INIT--------------------------
    t = threading.Thread(target=LCD)
    t.start()

    thread_sensors_init()
    thread_main_light_init()
    thread_heater_init()
    thread_heater_pwm_control_init()
    thread_sprayer_init()
    #--------------- OTHERS -------------------------
    terrarium.czasWyslania=datetime.datetime.now()
    czasUruchomieniaMenu=datetime.datetime.now()
    #---------SOCKET INIT--------
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    #--------------MAIN FUNCTION------------------------------
    while(1):
        #---------------WYSYLANIE------------------------
        if((datetime.datetime.now() - terrarium.czasWyslania)>(datetime.timedelta(minutes=terrarium.interwalWysylania))):
            msgFromClient = "terrarium.T:{:4.1f}/W:{:3.0f},t:{:4.1f}/w:{:3.0f}/I:{:9.4f}".format(terrarium.tempG,terrarium.wilgG,terrarium.tempD,terrarium.wilgD,terrarium.UVI)
            bytesToSend = str.encode(msgFromClient)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            terrarium.czasWyslania=datetime.datetime.now()
            log.add_log("Temp1: {:.1f} C / Wilg1: {:.0f}%RH  /  Temp2: {:.1f} C / Wilg2: {:.0f}%RH  /  UVA: {:.2f}, UVB: {:.2f}, UVI:{:.4f}".format(terrarium.tempG,terrarium.wilgG,terrarium.tempD,terrarium.wilgD,terrarium.UVA,terrarium.UVB,terrarium.UVI))
            #log.add_log("!stuff flag_ster_man: {:.1f} / flag_ster_ogrzew: {:.1f}".format(lampaHalogen.FlagaSterowanieManualne, lampaHalogen.FlagaSterowanieOgrzewaniem))
            log.add_log("!stuff czas do resetu: {}".format(terrarium.licznikOczekiwaniaNaCzujniki))

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                terrarium.runFlag = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px=event.pos[0]
                py=event.pos[1]
                czasUruchomieniaMenu=datetime.datetime.now()
                #zapis_dziennika_zdarzen ("You pressed the left mouse button at ({}, {})".format(px,py))
                #+++++OBSLUGA DOTYKU WYSWIETLACZA +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #--- strona 0 (glowna)----------
                if(aktywnaStrona==0):
                    if(px>0 and px<400 and py>0 and py<480):
                        aktywnaStrona=1
                        pygame.event.clear
                    elif(px>630 and px<800 and py>0 and py<150):
                        terrarium.runFlag = False
                        time.sleep(1)
                        pygame.quit()
                        sys.exit()
                        pygame.event.clear
                #---strona 1 (menu)-------------
                elif(aktywnaStrona==1):
                    if(px>30 and px<330 and py>60 and py<180):
                        aktywnaStrona=2
                        pygame.event.clear
                    elif(px>30 and px<330 and py>220 and py<340):
                        aktywnaStrona=3
                        pygame.event.clear
                    elif(px>690 and px<800 and py>390 and py<480):
                        aktywnaStrona=0
                        pygame.event.clear
                #---strona 2 (spryskanie)-------------
                elif(aktywnaStrona==2):
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
                        if(sprayer.czasSpryskiwania > 5):
                            sprayer.czasSpryskiwania -= 2
                    if(px>710 and px<790 and py>270 and py<350):  #czas spryskiwania +
                        if(sprayer.czasSpryskiwania < 50):
                            sprayer.czasSpryskiwania += 2
                    #--------
                    if(px>530 and px<610 and py>380 and py<480):  #spryskiwanie manualne
                        sprayer.spray_terrarium(sprayer.czasSpryskiwania)
                        pygame.event.clear
                    if(px>240 and px<320 and py>380 and py<430): #sprysk manualne -
                        if(sprayer.czasSpryskManual>5):
                            sprayer.czasSpryskManual-=2
                    if(px>240 and px<320 and py>430 and py<480):  #sprysk manualne +
                        sprayer.czasSpryskManual+=2
                    if(px>690 and px<800 and py>390 and py<480):
                        aktywnaStrona=1
                #---------------------
        czas1=datetime.datetime.now()-czasUruchomieniaMenu #powrot do glownego ekranu jesli bezczynny
        if(czas1.total_seconds()>=120):  # po dwoch minutach
            aktywnaStrona=0

        #BLOK KONTROLI DZIALANIA CZUJNIKOW
        #odejmuje 1 od ustawionego czasu; gdy odczyt poprawny przywraca wartosc ustawiona
        terrarium.licznikOczekiwaniaNaCzujniki=terrarium.licznikOczekiwaniaNaCzujniki-1
        if(terrarium.licznikOczekiwaniaNaCzujniki<1):
            print('RESET!')
            os.system('sudo shutdown -r now')

        time.sleep(.5)
    pass

if __name__ == '__main__':
    main()
