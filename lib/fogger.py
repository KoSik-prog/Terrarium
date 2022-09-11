#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        fogger
#
# Author:      KoSik
#
# Created:     11.09.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    import threading
    from timeit import default_timer as timer
    from terrarium import *
    from lib.log import *
    from lib.inout import *
except ImportError:
    print("Import error - fogger")
    
    
class Fogger:
    manualControlFlag = False
    timeLastUpdatePwm = 0  # variable to save the time of the last adjustment
    threadFlag = False

    def __init__(self, pin):
        self.pin = pin
        gpio.set_as_output(self.pin)
        self.timeLastUpdatePwm = datetime.datetime.now()
        
    def fogger_thread(self):
        if self.threadFlag == False:
            self.threadFlag = True
            gpio.fogger_on(self.pin)
            log.add_log("fogger on")
            time.sleep(600)
            gpio.fogger_off(self.pin)
            log.add_log("fogger off")
            self.threadFlag = False
        else:
            print("wait!")
    
    def fog_auto_run(self):
        foggerTH = threading.Thread(target=self.fogger_thread)
        foggerTH.start()
        
    def fog_on(self):
        gpio.fogger_on(self.pin)
        log.add_log("fogger on")
        
    def fog_off(self):
        gpio.fogger_off(self.pin)
        log.add_log("fogger off")
        

fogger = Fogger(16)