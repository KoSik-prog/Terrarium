#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        heater
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import datetime, PID
import RPi.GPIO as GPIO
from timeit import default_timer as timer

from terrarium import *
from libraries.log import *


class heaterCL:
    pwm=0
    pwmWymagane=0
    flag=False
    AutoON='11:00:00.0000'
    AutoOFF='15:30:00.0000'
    manualControlFlag=False
    heatControlFlag=False
    czasPWMustawienie=1.0 #ustawienie czasu narastania pwm
    czasPWM=0 #zmienna do zapisania czasu ostatniej regulacji
    pid = PID.PID(3, 4, 5)

    def __init__(self, pin, frequency):
        GPIO.setup(pin, GPIO.OUT) #set as output
        self.halogen = GPIO.PWM(pin, frequency)  # DAC start
        self.halogen.start(self.pwm)
        self.czasPWM = datetime.datetime.now()
        #--- PID settings -----
        self.pid.SetPoint = terrarium.tempWymaganaNaWyspie
        self.pid.setSampleTime(60)

    def heaterThread(self): #---- THREAD
        while terrarium.runFlag == True:
            self.check_timer()
            terrarium.heaterLastUpdateTime = datetime.datetime.now()
            time.sleep(10)

    def pwmControlThread(self): #---- THREAD
        while terrarium.runFlag == True:
            duration = datetime.datetime.now() - self.czasPWM
            if(duration.total_seconds() >= self.czasPWMustawienie):
                if(self.pwm > self.pwmWymagane):
                    self.pwm-=1
                    halogen.start(self.pwm)
                elif (self.pwm < self.pwmWymagane):
                    self.pwm+=1
                    halogen.start(self.pwm)
                self.czasPWM = datetime.datetime.now()
            if(self.pwm > 0):
                self.flag = True
            else:
                self.flag = False
            time.sleep(.1)

    def check_timer(self):
        format = '%H:%M:%S.%f'
        aktual=datetime.datetime.now().time()
        try:
            zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(self.AutoON, format) # obliczenie roznicy czasu
        except ValueError as e:
            print('Blad czasu wł:', e)
        try:
            zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(self.AutoOFF, format) # obliczenie roznicy czasu
        except ValueError as e:
            print('Blad czasu wył:', e)
        #-----skasowanie flag ----------
        if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  self.manualControlFlag==True):
            self.manualControlFlag=False
        if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and self.manualControlFlag==True):
            self.manualControlFlag=False
        #------SPRAWDZENIE------------------------
        if(self.heatControlFlag==False and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and self.manualControlFlag==False):
            self.czasPWMustawienie=1.0
            self.heatControlFlag=True
            log.add_log("AUTO Heater -> ON")
        if(self.heatControlFlag==True and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60)): # and self.manualControlFlag==False):# and s.is_alive()==True):
            log.add_log("AUTO Heater -> OFF")
            self.heatControlFlag=False
            self.pwmWymagane=0

    def sterowanieOgrzewaniem():
        if(terrarium.UVI > terrarium.minUVIdlaOgrzewania and self.manualControlFlag == True): #jesli kameleon nie zasłania swiatla
            self.pid.update(terrarium.tempG)
            if(self.manualControlFlag == True):
                self.pwm = self.pid.output
                self.pwmWymagane = max(min( int(pwm), 100 ),0)
                log.add_log("uvi: {:.2f} / temp: {:.2f} -> halog: {}".format(terrarium.UVI, terrarium.tempG, self.pwmWymagane))
                log.add_log("flagSterOgrz: {}".format(self.manualControlFlag))

    def heater_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def heater_off(self, pin):
        GPIO.output(pin, GPIO.LOW)



heater = heaterCL(13, 50)