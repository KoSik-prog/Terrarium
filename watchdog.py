# -------------------------------------------------------------------------------
# Name:        watchdog main program
# Purpose:
#
# Author:      kosik
#
# Created:     21.05.2020
# Copyright:   (c) kosik 2020
# -------------------------------------------------------------------------------
try:
    from lib.log import *
    from lib.watchdog import *
    import xml.etree.cElementTree as ET
    import time
    import os
except ImportError:
    print("Import error - communication")


if __name__ == "__main__":
    watchdog = Watchdog('Desktop/Home/watchdog.xml')
    watchdog.start()
