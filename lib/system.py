#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        system
# Purpose:
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
from lib.log import *

class System:
    def restart(self, message):
        log.add_error_log(message)
        #os.system('sudo shutdown -r now')

system = System()