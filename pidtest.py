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
import glob, time, sys, datetime, threading, os, PID

targetT = 26
P = 7
I = 3
D = 4
pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(0.1)
#+++++++++++++++++++++MAIN+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    v=0
    wejscie=25
    pwm=0
    exit=0
    while(exit==0):
        v+=1
        pid.update(wejscie)
        pwm = pid.output
        pwm = max(min( int(pwm), 100 ),0)
        wejscie+=((pwm-50)/100)
        print("we: {:.2f}    /    wy: {:.0f}".format(wejscie,pwm))
        time.sleep(0.1)
        if(v==120):
            exit=1


if __name__ == '__main__':
    main()
