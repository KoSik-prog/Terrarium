#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KoSik
#
# Created:     06.08.2020
# Copyright:   (c) kosik 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame, pygame.mixer, pygame.gfxdraw, glob, time, sys, datetime, smbus, board, busio, adafruit_veml6075, socket, threading, os, ekran
import RPi.GPIO as GPIO
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
import xml.etree.cElementTree as ET

from timeit import default_timer as timer

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT) #dripper ENABLE pin
GPIO.setup(20, GPIO.OUT) #dripper STEP
GPIO.setup(16, GPIO.OUT) #dripper DIR

#+++++++++++++++++++++MAIN+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dripperPompa(iloscKrokow, czasMs, kierunek):
    GPIO.output(12, GPIO.LOW)  #enable
    if(kierunek==0):
        GPIO.output(16, GPIO.HIGH) #kierunek
    else:
        GPIO.output(16, GPIO.LOW) #kierunek

    for x in range(int(iloscKrokow)):
        GPIO.output(20, GPIO.HIGH)
        time.sleep(czasMs)
        GPIO.output(20, GPIO.LOW)
        time.sleep(czasMs)
    GPIO.output(12, GPIO.HIGH) #disable
    GPIO.output(16, GPIO.LOW) #kierunek


def main():
    global watekAktywny, czasStartu, aktywnaStrona
    print('START!!!')

    dripperPompa(20000, .0001, 0)

    for x in range(0,10):
        dripperPompa(4000, .0001, 0)
        time.sleep(6)

    print('STOP!')

if __name__ == '__main__':
    main()
