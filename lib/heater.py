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
import datetime, PID, threading
from timeit import default_timer as timer

from terrarium import *
from lib.log import *
from lib.inout import *

class heater_CL:
    pwmRequired = 0
    manualControlFlag = False
    heatControlFlag = False
    pmwChangeTime = 1#s czas w sekundach pomiedzy kazdym %PWM
    dimmingTime = 3 #s czas w sekundach pomiedzy kazdym %PWM dla ściemniania
    timeLastUpdatePwm = 0 #zmienna do zapisania czasu ostatniej regulacji
    pid = PID.PID(3, 4, 5)

    def __init__(self, pin, frequency, autoOn, autoOff):
        gpio.set_as_dac(pin, frequency)
        self.timeLastUpdatePwm = datetime.datetime.now()
        self.AutoON = autoOn
        self.AutoOFF = autoOff
        #--- PID settings -----
        self.pid.SetPoint = terrarium.read_requred_island_temperature()
        self.pid.setSampleTime(60)

    def heater_thread(self): #---- THREAD
        while terrarium.runFlag == True:
            self.check_timer()
            terrarium.heaterLastUpdateTime = datetime.datetime.now()
            time.sleep(10)

    def pwm_control_thread(self): #---- THREAD
        i = 0
        while terrarium.runFlag == True:
            if self.heatControlFlag == True:
                duration = datetime.datetime.now() - self.timeLastUpdatePwm
                if(duration.total_seconds() >= self.pmwChangeTime):
                    if(gpio.read_heater_pwm() > self.pwmRequired):
                        gpio.set_heater_pwm(gpio.read_heater_pwm() - 1)
                    elif (gpio.read_heater_pwm() < self.pwmRequired):
                        gpio.set_heater_pwm(gpio.read_heater_pwm() + 1)
                    self.timeLastUpdatePwm = datetime.datetime.now()
                if(i == 10): # 1sec
                    self.heating_control()
                    i = 0
                i += 1
                time.sleep(.1)
            else:
                break
        while gpio.check_heater_flag() == True: #dimming
            duration = datetime.datetime.now() - self.timeLastUpdatePwm
            if(duration.total_seconds() >= self.dimmingTime):
                gpio.set_heater_pwm(gpio.read_heater_pwm() - 1)
                self.timeLastUpdatePwm = datetime.datetime.now()
            time.sleep(.1)


    def check_timer(self):
        format = '%H:%M:%S.%f'
        actualTime=datetime.datetime.now().time()
        try:
            stampOn = datetime.datetime.strptime(str(actualTime), format) - datetime.datetime.strptime(self.AutoON, format) # obliczenie roznicy czasu
        except ValueError as e:
            log.add_error_log('error:', e)
        try:
            stampOff = datetime.datetime.strptime(str(actualTime), format) - datetime.datetime.strptime(self.AutoOFF, format) # obliczenie roznicy czasu
        except ValueError as e:
            log.add_error_log('error:', e)
        #----- clear flags ----------
        if(int(stampOn.total_seconds())>(-15) and int(stampOn.total_seconds())<0 and  self.manualControlFlag==True):
            self.manualControlFlag=False
        if(int(stampOff.total_seconds())>(-15) and int(stampOff.total_seconds())<0 and self.manualControlFlag==True):
            self.manualControlFlag=False
        #------ check ------------------------
        if(self.heatControlFlag==False and (int(stampOn.total_seconds())>0) and (int(stampOff.total_seconds())<(-60)) and self.manualControlFlag==False):
            self.pmwChangeTime=1.0
            self.heatControlFlag=True
            heaterPwmControlTH = threading.Thread(target = self.pwm_control_thread)
            log.add_log("AUTO Heater -> ON")
            heaterPwmControlTH.start()  #run thread
        if(self.heatControlFlag==True and (int(stampOff.total_seconds())>0) and (int(stampOff.total_seconds())<60)): # and self.manualControlFlag==False):# and s.is_alive()==True):
            log.add_log("AUTO Heater -> OFF")
            self.heatControlFlag=False
            self.pwmRequired=0

    def heating_control(self):
        if(terrarium.UVI > terrarium.minUviForHeating and self.heatControlFlag == True): #jesli kameleon nie zasłania swiatla
            self.pid.update(terrarium.temperatureTop)
            if(self.heatControlFlag == True):
                self.pwmRequired = max(min( int(self.pid.output), 100 ),0)
                #log.add_log("uvi: {:.2f} / temp: {:.2f} -> halog: {} / flagSterOgrz: {}".format(terrarium.UVI, terrarium.temperatureTop, self.pwmRequired, self.heatControlFlag))

heater = heater_CL(13, 50, '11:00:00.0000', '17:30:00.0000')