#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        terrarium
#
# Author:      KoSik
#
# Created:     27.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import sys
    import smbus
    import board
    import busio
    import adafruit_veml6075
    import time
except ImportError:
    print("Import error - communication")


class Bus:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.veml = None
        time.sleep(0.1)

    def bus_init(self):
        self.veml = adafruit_veml6075.VEML6075(self.i2c, integration_time=100)
        time.sleep(0.5)

    def read(self):
        self.bus_init()
        print(self.veml.uva)


bus = Bus()


class Temp():
    def __init__(self):
        self.i2cbus = None

    def start(self):
        self.i2cbus = smbus.SMBus(1)

    def stop(self):
        del self.i2cbus

    def readtest(self):
        try:
            self.i2cbus.write_i2c_block_data(0x44, 0x2C, [0x06])
        except pigpio.error as e:
            print("error: %s" % (e))

        time.sleep(0.5)
        try:
            data = self.i2cbus.read_i2c_block_data(0x44, 0x00, 6)
        except IOError:
            zapis_dziennika_zdarzen('err')
        sens = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
        print(sens)


temp = Temp()


def main():
    temp.start()
    temp.readtest()
    temp.stop()
    temp.start()
    temp.readtest()
    testi2c = busio.I2C(board.SCL, board.SDA)
    testbus = adafruit_veml6075.VEML6075(testi2c, integration_time=100)
    time.sleep(0.5)
    print(testbus.uva)

    """for i in range(10):
        print(i)
        bus.read()
        time.sleep(0.5)
        if i == 4:
            del veml"""


if __name__ == '__main__':
    main()
