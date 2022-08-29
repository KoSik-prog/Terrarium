#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        inout
#              GPIO module
#
# Author:      KoSik
#
# Created:     29.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import RPi.GPIO as GPIO
from libraries.log import *

class gpio_CL:
    halogen = None
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(12, GPIO.OUT) #dripper ENABLE pin
        #GPIO.setup(20, GPIO.OUT) #dripper STEP
        #GPIO.setup(16, GPIO.OUT) #dripper DIR

    def set_heater_pwm(self, pwm):
        self.halogen.start(self.pwm)

    def set_as_dac(self, pin, frequency): #PWM
        self.set_as_output(pin)
        self.halogen = GPIO.PWM(pin, frequency)  # DAC start
        self.halogen.start(0)

    def set_as_output(self, pin):
        GPIO.setup(pin, GPIO.OUT)

    def sprayer_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def sprayer_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

    def lamp_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def lamp_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

gpio = gpio_CL()