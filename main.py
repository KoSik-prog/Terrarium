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
import pygame, pygame.mixer, pygame.gfxdraw, glob, time, sys, datetime, smbus, board, busio, adafruit_veml6075, socket, threading, os
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
from libraries.display import *
from libraries.gui import *
from terrarium import *
#+++++++ZMIENNE++++++++++++++++++++++++++++++++++++++
kolorczcionki=(185,242,107,255)
tfps=1

serverAddressPort = ("192.168.0.99", 2222)
bufferSize = 1024
#+++++++++++++++++++++ DELAY +++++++++++++++++++++++++++
time.sleep(10)
#+++++++++++++++++++++++++++++WE/WY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GPIO.setmode(GPIO.BCM)
#GPIO.setup(12, GPIO.OUT) #dripper ENABLE pin
#GPIO.setup(20, GPIO.OUT) #dripper STEP
#GPIO.setup(16, GPIO.OUT) #dripper DIR
######################################################################################
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
#++++++++++++++++ THREADS DEFINITIONS ++++++++++++++++++++++++++++++++++++++++++++++++++
def thread_sensors_init():
    sensorsTH = threading.Thread(target = sensors.sensors_thread)
    sensorsTH.start()

def thread_main_light_init():
    mainLightTH = threading.Thread(target = mainLight.main_light_thread)
    mainLightTH.start()

def thread_heater_init():
    heaterTH = threading.Thread(target = heater.heater_thread)
    heaterTH.start()

def thread_heater_pwm_control_init():
    heaterPwmControlTH = threading.Thread(target = heater.pwm_control_thread)
    heaterPwmControlTH.start()

def thread_sprayer_init():
    sprayerTH = threading.Thread(target = sprayer.sprayer_thread)
    sprayerTH.start()

def thread_gui_init():
    guiTH = threading.Thread(target = gui.gui_thread)
    guiTH.start()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    log.add_log("Starting...")

    zapis_ustawien_xml()
    odczyt_ustawien_xml()
    #-------------THREADS INIT--------------------------
    thread_sensors_init()
    thread_main_light_init()
    thread_heater_init()
    thread_heater_pwm_control_init()
    thread_sprayer_init()
    thread_gui_init()
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
                if(gui.aktywnaStrona==0):
                    if(px>0 and px<400 and py>0 and py<480):
                        gui.aktywnaStrona=1
                        pygame.event.clear
                    elif(px>630 and px<800 and py>0 and py<150):
                        terrarium.runFlag = False
                        time.sleep(1)
                        pygame.quit()
                        sys.exit()
                        pygame.event.clear
                #---strona 1 (menu)-------------
                elif(gui.aktywnaStrona==1):
                    if(px>30 and px<330 and py>60 and py<180):
                        gui.aktywnaStrona=2
                        pygame.event.clear
                    elif(px>30 and px<330 and py>220 and py<340):
                        gui.aktywnaStrona=3
                        pygame.event.clear
                    elif(px>690 and px<800 and py>390 and py<480):
                        gui.aktywnaStrona=0
                        pygame.event.clear
                #---strona 2 (spryskanie)-------------
                elif(gui.aktywnaStrona==2):
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
                        gui.aktywnaStrona=1
                #---------------------
        czas1=datetime.datetime.now()-czasUruchomieniaMenu #powrot do glownego ekranu jesli bezczynny
        if(czas1.total_seconds()>=120):  # po dwoch minutach
            gui.aktywnaStrona=0
        time.sleep(.5)
    pass

if __name__ == '__main__':
    main()
