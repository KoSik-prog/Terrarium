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
import pygame, pygame.mixer, pygame.gfxdraw, glob, time, sys, datetime, smbus, board, busio, adafruit_veml6075, socket, threading, os, ekran, PID
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
from terrarium import *
#+++++++ZMIENNE++++++++++++++++++++++++++++++++++++++
bgcolor=(0,0,0,255)
kolorczcionki=(185,242,107,255)
tfps=1

serverAddressPort = ("192.168.0.99", 2222)
bufferSize = 1024

watekAktywny=0
czasStartu=0

aktywnaStrona=0 #strona do wyswietlenia
#+++++++++++++++++++++ ZWLOKA CZASOWA +++++++++++++++++++++++++++
time.sleep(10)

mainLight = MAIN_LIGHT_CL('8:00:00.0000', '19:15:00.0000')

class lampaHalogenCl: #Halogen
    pwm=0
    pwmWymagane=0
    Flaga=False
    AutoON='11:00:00.0000'
    AutoOFF='15:30:00.0000'
    FlagaSterowanieManualne=False
    FlagaSterowanieOgrzewaniem=False
    czasPWMustawienie=1.0 #ustawienie czasu narastania pwm
    czasPWM=0 #zmienna do zapisania czasu ostatniej regulacji
lampaHalogen=lampaHalogenCl

class spryskiwaczCl:   #TERRARIUM
    on1H=9
    on1M=0
    on2H=15
    on2M=0
    czasSpryskiwania=12
    czasSpryskManual=5
    flaga=False
    ostatnieSpryskanie=0
spryskiwacz=spryskiwaczCl

#+++++++++++++++++++++++++++++WE/WY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT) #Halogen
#GPIO.setup(12, GPIO.OUT) #dripper ENABLE pin
#GPIO.setup(20, GPIO.OUT) #dripper STEP
#GPIO.setup(16, GPIO.OUT) #dripper DIR
GPIO.setup(19, GPIO.OUT) #Metalohalogen
GPIO.setup(21, GPIO.OUT) #spryskiwacz

halogen = GPIO.PWM(13, 50)  # uruchomienie PWM Halogenu
halogen.start(lampaHalogen.pwm)

#GPIO.output(12, GPIO.HIGH) #dripper enable pin - motor disable
#GPIO.output(19, GPIO.LOW) #Metalohalogen 0
#+++++++++++++++++++++++++ inne ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#---ustawienia PID----
targetT = terrarium.tempWymaganaNaWyspie
P = 3 #3
I = 4 #2
D = 5 #5

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(60)
print("Kp: {}, Ki: {}, Kd: {}, Target: {}".format(pid.Kp,pid.Ki,pid.Kd,pid.SetPoint))
######################################################################################

def timerHalogen():
    format = '%H:%M:%S.%f'
    aktual=datetime.datetime.now().time()
    try:
        zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(lampaHalogen.AutoON, format) # obliczenie roznicy czasu
    except ValueError as e:
        print('Blad czasu wł:', e)
    try:
        zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(lampaHalogen.AutoOFF, format) # obliczenie roznicy czasu
    except ValueError as e:
        print('Blad czasu wył:', e)
    #-----skasowanie flag ----------
    if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  lampaHalogen.FlagaSterowanieManualne==True):
        lampaHalogen.FlagaSterowanieManualne=False
    if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and lampaHalogen.FlagaSterowanieManualne==True):
        lampaHalogen.FlagaSterowanieManualne=False
    #------SPRAWDZENIE------------------------
    if(lampaHalogen.FlagaSterowanieOgrzewaniem==False and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and lampaHalogen.FlagaSterowanieManualne==False):
        lampaHalogen.czasPWMustawienie=1.0
        lampaHalogen.FlagaSterowanieOgrzewaniem=True
        log.add_log("AUTO Halogen -> ON")
    if(lampaHalogen.FlagaSterowanieOgrzewaniem==True and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60)): # and lampaHalogen.FlagaSterowanieManualne==False):# and s.is_alive()==True):
        log.add_log("AUTO Halogen -> OFF")
        lampaHalogen.FlagaSterowanieOgrzewaniem=False
        lampaHalogen.pwmWymagane=0

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

    """if(lampaMHG.Flaga==1):
        ekran.icons(10,pozycjaIkon,255,"zarowka1")
        pozycjaIkon+=125"""

    if(lampaHalogen.Flaga==1):
        ekran.icons(10,pozycjaIkon,255,"zarowka2")
        dl=ekran.napis_centralny(screen, "{}%".format(lampaHalogen.pwm),"Nimbus Sans L",48,70,pozycjaIkon+50,(235,0,69),255)
        pozycjaIkon+=125

    if(spryskiwacz.flaga==1):
        ekran.icons(10,pozycjaIkon,255,"spryskiwacz")
        pozycjaIkon+=125

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

    ekran.napis(screen, "czas pracy:{}".format(str(datetime.timedelta(seconds=round(end-czasStartu)))),"Nimbus Sans L",30,50,440,(150,150,150),100)

    ekran.przycisk(screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
    ekran.napis(screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
    pygame.display.update()

def menuSpryskiwacz():
    global screen

    end = timer()
    ekran.icons(0,0,255,"tlo")

    if(lampaMHG.Flaga==1):
        ekran.icons(10,10,255,"zarowka1")

    if(lampaHalogen.Flaga==1):
        ekran.icons(70,10,255,"zarowka2")

    ekran.napis(screen, "Timer 1: ","Nimbus Sans L",60,30,40,(253,180,165),255)
    ekran.przycisk(screen, (200,10,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,230,0,(15,15,15),255)
    ekran.przycisk(screen, (200,60,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,225,48,(220,220,220),255)
    ekran.przycisk(screen, (285,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(spryskiwacz.on1H),"Nimbus Sans L",120,290,17,(220,220,220),255)
    ekran.napis(screen, ":","Nimbus Sans L",120,382,15,(220,220,220),255)
    ekran.przycisk(screen, (400,10,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(spryskiwacz.on1M),"Nimbus Sans L",120,405,17,(220,220,220),255)
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
    ekran.napis(screen, "{:02d}".format(spryskiwacz.on2H),"Nimbus Sans L",120,290,147,(220,220,220),255)
    ekran.napis(screen, ":","Nimbus Sans L",120,382,145,(220,220,220),255)
    ekran.przycisk(screen, (400,140,100,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{:02d}".format(spryskiwacz.on2M),"Nimbus Sans L",120,405,147,(220,220,220),255)
    ekran.przycisk(screen, (505,140,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,535,130,(15,15,15),255)
    ekran.przycisk(screen, (505,190,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,530,178,(220,220,220),255)

    ekran.napis(screen, "Czas spryskiwania: ","Nimbus Sans L",60,30,290,(253,180,165),255)
    ekran.przycisk(screen, (420,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",110,450,264,(15,15,15),255)
    ekran.przycisk(screen, (505,270,200,80) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{} s".format(spryskiwacz.czasSpryskiwania),"Nimbus Sans L",80,535,280,(15,15,15),255)
    ekran.przycisk(screen, (710,270,80,80) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,736,274,(15,15,15),255)

    ekran.napis(screen, "Manualne: ","Nimbus Sans L",60,30,410,(253,180,165),255)
    ekran.przycisk(screen, (240,380,80,50) ,(200,200,200), (250,250,250), 10, 2)
    ekran.napis(screen, "-","Nimbus Sans L",90,270,370,(15,15,15),255)
    ekran.przycisk(screen, (240,430,80,50) ,(80,80,80), (50,50,50), 10, 2)
    ekran.napis(screen, "+","Nimbus Sans L",80,265,420,(220,220,220),255)
    ekran.przycisk(screen, (325,380,200,100) ,(55,112,21), (55,112,21), 10, 2)
    ekran.napis(screen, "{} s".format(spryskiwacz.czasSpryskManual),"Nimbus Sans L",80,350,400,(220,220,220),255)
    ekran.przycisk(screen, (530,380,80,100) ,(20,192,21), (30,220,21), 10, 2)

    ekran.napis(screen, "ostatnie:","Nimbus Sans L",40,670,20,(253,201,77),255)
    ekran.napis(screen, "{}".format(str(datetime.timedelta(seconds=round(end-spryskiwacz.ostatnieSpryskanie)))),"Nimbus Sans L",40,670,60,(253,201,77),255)

    ekran.przycisk(screen, (690,390,100,80) ,(120,120,120), (15,15,15), 10, 2)
    ekran.napis(screen, "<","Nimbus Sans L",120,716,375,(0,0,0),255)
    pygame.display.update()

def LCD():  #----WYSWIETLANIE - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
    global watekAktywny , aktywnaStrona
    tfps=0.5

    while(watekAktywny==1):
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

def sterowanieOgrzewaniem():
    if(terrarium.UVI > terrarium.minUVIdlaOgrzewania and lampaHalogen.FlagaSterowanieOgrzewaniem == True): #jesli kameleon nie zasłania swiatla
        pid.update(terrarium.tempG)
        if(lampaHalogen.FlagaSterowanieOgrzewaniem == True):
            pwm = pid.output
            lampaHalogen.pwmWymagane = max(min( int(pwm), 100 ),0)
            log.add_log("uvi: {:.2f} / temp: {:.2f} -> halog: {}".format(terrarium.UVI, terrarium.tempG, lampaHalogen.pwmWymagane))
            log.add_log("flagSterOgrz: {}".format(lampaHalogen.FlagaSterowanieOgrzewaniem))
#++++++++++++++++WĄTKI+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def licznik():  #-----------watek timera
    global watekAktywny
    czas1='09'  #w tych godzinach aktywne dodatkowe spryskiwanie
    czas2='18'
    GPIO.output(21, GPIO.LOW)

    while(watekAktywny==1):
        end = timer()
        teraz = datetime.datetime.now()
        czasik=('{:02d}:{:02d}'.format(teraz.hour,teraz.minute))
        czasikON1=('{:02d}:{:02d}'.format(spryskiwacz.on1H,spryskiwacz.on1M))
        czasikON2=('{:02d}:{:02d}'.format(spryskiwacz.on2H,spryskiwacz.on2M))
        if(czasik==czasikON1 or czasik==czasikON2):
            log.add_log('Spryskiwanie!')
            GPIO.output(21, GPIO.HIGH)
            time.sleep(int(spryskiwacz.czasSpryskiwania))
            GPIO.output(21, GPIO.LOW)
            spryskiwacz.ostatnieSpryskanie= timer()
            time.sleep(30)
        #-------------------------------------
        if(int(teraz.hour) >= int(czas1) and int(teraz.hour) <= int(czas2)):
            if(terrarium.wilgD > 5 and terrarium.wilgD < terrarium.minWilgotnosc and (end-spryskiwacz.ostatnieSpryskanie)>300):
                log.add_log('Dodatkowe spryskiwanie!')
                GPIO.output(21, GPIO.HIGH)
                time.sleep(int(spryskiwacz.czasSpryskiwania))
                GPIO.output(21, GPIO.LOW)
                spryskiwacz.ostatnieSpryskanie= timer()
                time.sleep(30)
        #------------
        mainLight.check_timer(czasStartu)
        timerHalogen()
        time.sleep(10)

def odczytCzujnikowWatek(): # ODCZYT CZUJNIKOW--- WATEK!!!!!!!!!!!!! --------------------------------------------------------------------------------------
    i=0
    while(watekAktywny==1):
        i+=1
        sensors.read_light_index()
        sensors.read_temperatures()
        terrarium.UVA = sensors.UVA # poprawić!
        terrarium.UVB = sensors.UVB
        terrarium.UVI = sensors.UVI
        if (i>=10):
            sterowanieOgrzewaniem()
            i=0
        #sprawdzenie czy czujnik nie zawiesił się
        if(terrarium.tempD != terrarium.staraTempD or terrarium.tempG != terrarium.staraTempG or terrarium.wilgD != terrarium.staraWilgD or terrarium.wilgG != terrarium.staraWilgG or terrarium.UVA != terrarium.staraUVA):
            duration = datetime.datetime.now() - terrarium.ostatnieOdswiezenieCzujnikow
            #zapis_dziennika_zdarzen ("czujniki dzialaja / czas: {:.0f}".format(duration.total_seconds()))
            #--------------
            terrarium.staraTempD = terrarium.tempD
            terrarium.staraTempG = terrarium.tempG
            terrarium.staraWilgD= terrarium.wilgD
            terrarium.staraWilgG = terrarium.wilgG
            terrarium.staraUVA = terrarium.UVA
            terrarium.ostatnieOdswiezenieCzujnikow = datetime.datetime.now()

        time.sleep(1)
        terrarium.licznikOczekiwaniaNaCzujniki=terrarium.czasOczekiwaniaNaCzujniki*60 #poprawny odczyt resetuje licznik bledu

def sterowanieHalogenem(): #-----sterowanie halogenem WĄTEK
    global watekAktywny
    while(watekAktywny==1):
        duration = datetime.datetime.now() - lampaHalogen.czasPWM
        if(duration.total_seconds() >= lampaHalogen.czasPWMustawienie):
            if(lampaHalogen.pwm > lampaHalogen.pwmWymagane):
                lampaHalogen.pwm-=1
                halogen.start(lampaHalogen.pwm)
            elif (lampaHalogen.pwm < lampaHalogen.pwmWymagane):
                lampaHalogen.pwm+=1
                halogen.start(lampaHalogen.pwm)
            lampaHalogen.czasPWM = datetime.datetime.now()
        if(lampaHalogen.pwm>0):
            lampaHalogen.Flaga=True
        else:
            lampaHalogen.Flaga=False
        time.sleep(.1)
#+++++++++++++++++++++MAIN+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    global watekAktywny, czasStartu, aktywnaStrona

    terrarium.licznikOczekiwaniaNaCzujniki=120*60

    lampaHalogen.czasPWM = datetime.datetime.now()
    terrarium.ostatnieOdswiezenieCzujnikow = datetime.datetime.now()

    czasStartu = timer()
    spryskiwacz.ostatnieSpryskanie= timer()

    zapis_ustawien_xml()
    odczyt_ustawien_xml()

    watekAktywny=1
    t=threading.Thread(target=LCD)
    t.start()
    c=threading.Thread(target=odczytCzujnikowWatek)
    c.start()
    t1=threading.Thread(target=licznik)
    t1.start()
    st=threading.Thread(target=sterowanieHalogenem)
    st.start()

    terrarium.czasWyslania=datetime.datetime.now()
    czasUruchomieniaMenu=datetime.datetime.now()
    #---------SOCKET INIT--------
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
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
                watekAktywny=0
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
                        watekAktywny=0
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
                        spryskiwacz.on1H-=1
                        if(spryskiwacz.on1H<0):
                            spryskiwacz.on1H=23
                    if(px>200 and px<280 and py>60 and py<110): #godz1 +
                        spryskiwacz.on1H+=1
                        if(spryskiwacz.on1H>23):
                            spryskiwacz.on1H=0
                    if(px>505 and px<585 and py>10 and py<60):  #min1 -
                        spryskiwacz.on1M-=1
                        if(spryskiwacz.on1M<0):
                            spryskiwacz.on1M=59
                    if(px>505 and px<585 and py>60 and py<110): #min1 +
                        spryskiwacz.on1M+=1
                        if(spryskiwacz.on1M>59):
                            spryskiwacz.on1M=0
                    #--------
                    if(px>200 and px<280 and py>140 and py<190):  #godz2 -
                        spryskiwacz.on2H-=1
                        if(spryskiwacz.on2H<0):
                            spryskiwacz.on2H=23
                    if(px>200 and px<280 and py>190 and py<240): #godz2 +
                        spryskiwacz.on2H+=1
                        if(spryskiwacz.on2H>23):
                            spryskiwacz.on2H=0
                    if(px>505 and px<585 and py>140 and py<190):  #min2 -
                        spryskiwacz.on2M-=1
                        if(spryskiwacz.on2M<0):
                            spryskiwacz.on2M=59
                    if(px>505 and px<585 and py>190 and py<240): #min2 +
                        spryskiwacz.on2M+=1
                        if(spryskiwacz.on2M>59):
                            spryskiwacz.on2M=0
                    #--------
                    if(px>420 and px<500 and py>270 and py<350):  #czas spryskiwania -
                        if(spryskiwacz.czasSpryskiwania>5):
                            spryskiwacz.czasSpryskiwania-=2
                    if(px>710 and px<790 and py>270 and py<350):  #czas spryskiwania +
                        if(spryskiwacz.czasSpryskiwania<50):
                            spryskiwacz.czasSpryskiwania+=2
                    #--------
                    if(px>530 and px<610 and py>380 and py<480):  #spryskiwanie manualne
                        GPIO.output(21, GPIO.HIGH)
                        time.sleep(spryskiwacz.czasSpryskManual)
                        GPIO.output(21, GPIO.LOW)
                        log.add_log('Spryskiwanie manualne! -> {}sek'.format(spryskiwacz.czasSpryskManual))
                        spryskiwacz.ostatnieSpryskanie= timer()
                        pygame.event.clear
                    if(px>240 and px<320 and py>380 and py<430): #sprysk manualne -
                        if(spryskiwacz.czasSpryskManual>5):
                            spryskiwacz.czasSpryskManual-=2
                    if(px>240 and px<320 and py>430 and py<480):  #sprysk manualne +
                        spryskiwacz.czasSpryskManual+=2
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
