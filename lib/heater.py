#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        heater
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    import threading
    from timeit import default_timer as timer
    import PID
    from terrarium import *
    from lib.log import *
    from lib.inout import *
except ImportError:
    print("Import error - heater")


class Heater:
    pwmRequired = 0
    manualControlFlag = False
    heatControlFlag = False
    pmwChangeTime = 1  # s time in seconds between each %PWM
    dimmingTime = 3  # s time in seconds between each %PWM for dimming
    lightOffTime = 6 #s * 100 dimm time to light off
    timeLastUpdatePwm = 0  # variable to save the time of the last adjustment
    pid = PID.PID(3, 4, 5)

    def __init__(self, pin, frequency, autoOn, autoOff):
        gpio.set_as_dac(pin, frequency)
        self.timeLastUpdatePwm = datetime.datetime.now()
        self.autoOn = autoOn + ":00.0"
        self.autoOff = autoOff + ":00.0"
        # --- PID settings -----
        self.pid.SetPoint = terrarium.get_requred_island_temperature()
        self.pid.setSampleTime(60)
        gpio.set_heater_pwm(0)

    def heater_thread(self):
        while terrarium.runFlag == True:
            self.check_timer()
            terrarium.heaterLastUpdateTime = datetime.datetime.now()
            time.sleep(10)

    def pwm_control_thread(self):
        i = 0
        while terrarium.runFlag == True:
            if self.heatControlFlag == True:
                duration = datetime.datetime.now() - self.timeLastUpdatePwm
                if (duration.total_seconds() >= self.pmwChangeTime):
                    if (gpio.get_heater_pwm() > self.pwmRequired):
                        gpio.set_heater_pwm(gpio.get_heater_pwm() - 1)
                    elif (gpio.get_heater_pwm() < self.pwmRequired):
                        gpio.set_heater_pwm(gpio.get_heater_pwm() + 1)
                    self.timeLastUpdatePwm = datetime.datetime.now()
                if (i == 10):  # 1sec
                    self.heating_control()
                    i = 0
                i += 1
                time.sleep(.1)
            else:
                break
        while gpio.check_heater_flag() == True:  # dimming
            duration = datetime.datetime.now() - self.timeLastUpdatePwm
            if (duration.total_seconds() >= self.dimmingTime):
                gpio.set_heater_pwm(gpio.get_heater_pwm() - 1)
                self.timeLastUpdatePwm = datetime.datetime.now()
            time.sleep(.1)
            
    def dimm_light_thread(self):
        while gpio.check_heater_flag() == True:  # dimming
            duration = datetime.datetime.now() - self.timeLastUpdatePwm
            if (duration.total_seconds() >= self.lightOffTime):
                gpio.set_heater_pwm(gpio.get_heater_pwm() - 1)
                self.timeLastUpdatePwm = datetime.datetime.now()
            time.sleep(.1)

    def check_timer(self):
        format = '%H:%M:%S.%f'
        actualTime = datetime.datetime.now().time()
        try:
            stampOn = datetime.datetime.strptime(
                str(actualTime), format) - datetime.datetime.strptime(self.autoOn, format)
        except ValueError as e:
            log.add_error_log('error:', e)
        try:
            stampOff = datetime.datetime.strptime(
                str(actualTime), format) - datetime.datetime.strptime(self.autoOff, format)
        except ValueError as e:
            log.add_error_log('error:', e)
        # ----- clear flags ----------
        if (int(stampOn.total_seconds()) > (-15) and int(stampOn.total_seconds()) < 0 and self.manualControlFlag == True):
            self.manualControlFlag = False
        if (int(stampOff.total_seconds()) > (-15) and int(stampOff.total_seconds()) < 0 and self.manualControlFlag == True):
            self.manualControlFlag = False
        # ------ check ------------------------
        if (self.heatControlFlag == False and (int(stampOn.total_seconds()) > 0) and (int(stampOff.total_seconds()) < (-60)) and self.manualControlFlag == False): 
            self.heat_control_start()
        if (self.heatControlFlag == True and (int(stampOff.total_seconds()) > 0) and (int(stampOff.total_seconds()) < 60)):
            self.heat_control_stop()
            self.pwmRequired = 0
                      
    def heat_control_start(self):
        self.pmwChangeTime = 1.0
        self.heatControlFlag = True
        heaterPwmControlTH = threading.Thread(target=self.pwm_control_thread)
        log.add_log("AUTO Heater -> ON")
        heaterPwmControlTH.start()  # run thread
        
    def heat_control_stop(self):
        log.add_log("AUTO Heater -> OFF")
        self.heatControlFlag = False

    def heating_control(self):
        # if the light is not obstructed by the chameleon
        if (terrarium.uvi > terrarium.minUviForHeating and self.heatControlFlag == True):
            self.pid.update(terrarium.temperatureTop)
            if (self.heatControlFlag == True):
                self.pwmRequired = max(min(int(self.pid.output), 100), 0)
                #log.add_log("uvi: {:.2f} / temp: {:.2f} -> halog: {} / flagSterOgrz: {}".format(terrarium.uvi, terrarium.temperatureTop, self.pwmRequired, self.heatControlFlag))
                
    def update_pid_target(self):
        self.pid.SetPoint = terrarium.get_requred_island_temperature()
                
    def dim_light(self):
        self.heatControlFlag = False
        gpio.set_heater_pwm(100)
        dimmLightTH = threading.Thread(target=self.dimm_light_thread)
        dimmLightTH.start()  # run thread
        
    def set_heat_control_flag(self, flag):
        self.heatControlFlag = flag
        
    def get_heat_control_flag(self):
        return self.heatControlFlag
    
    def set_manual_control_flag(self, flag):
        self.manualControlFlag = flag


heater = Heater(13, 50, '11:00', '16:30')
