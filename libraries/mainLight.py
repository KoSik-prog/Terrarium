#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        mainLight
# Purpose:
#
# Author:      KoSik
#
# Created:     26.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import RPi.GPIO as GPIO


class MAIN_LIGHT:
    flag = False
    AutoON = '8:00:00.0000'
    AutoOFF = '19:15:00.0000'#'19:45:00.0000'
    dimmingTime = 12 #czas stopniowego wygaszania w minutach
    manualControlFlag = False

    def __init__(self, address):

    def lamp_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def lamp_off(self, pin):
        GPIO.output(pin, GPIO.LOW)